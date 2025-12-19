import csv
import os
from django.core.management.base import BaseCommand
from position.models import Section, Subsection, Class, Subclass, Group, Position


def get_code_level(code):
    """
    Determine the hierarchy level based on code structure.
    Returns: 'section', 'subsection', 'class', 'subclass', 'group', 'position'
    """
    code_str = str(code).strip()
    
    if '.' in code_str:
        return 'position'
    
    digits_only = ''.join(c for c in code_str if c.isdigit())
    digit_count = len(digits_only)
    
    if digit_count == 1:
        return 'section'
    elif digit_count == 2:
        return 'subsection'
    elif digit_count == 3:
        return 'class'
    elif digit_count == 4:
        return 'subclass'
    elif digit_count > 4:
        return 'group'
    
    return None


def get_parent_code(code, level):
    """
    Extract parent code based on current code and level.
    """
    code_str = str(code).strip()
    digits_only = ''.join(c for c in code_str if c.isdigit())
    
    if level == 'position':
        if '.' in code_str:
            return code_str.split('.')[0]
        return None
    
    if level == 'subclass':
        if len(digits_only) >= 3:
            return digits_only[:3]
        return None
    
    if level == 'class':
        if len(digits_only) >= 2:
            return digits_only[:2]
        return None
    
    if level == 'subsection':
        if len(digits_only) >= 1:
            return digits_only[0]
        return None
    
    return None


class Command(BaseCommand):
    help = 'Load Classification of Professions (KP) data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='temp/classification_of_professions.csv',
            help='Path to the KP CSV file'
        )

    def handle(self, *args, **options):
        file_path = options['file']
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return

        self.stdout.write(f'Loading data from {file_path}...')

        stats = {
            'sections': 0,
            'subsections': 0,
            'classes': 0,
            'subclasses': 0,
            'groups': 0,
            'positions': 0,
            'errors': 0
        }

        with open(file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=';')
            rows = list(reader)

        total_rows = len(rows)
        self.stdout.write(f'Found {total_rows} rows to process')

        # First pass: Import all codes without dots (Section, Subsection, Class, Subclass)
        # For 4-digit codes, we'll import them as Subclasses initially
        self.stdout.write('Pass 1: Importing non-position codes...')
        for idx, row in enumerate(rows, 1):
            if idx % 100 == 0:
                self.stdout.write(f'Processing row {idx}/{total_rows}...')

            code = row.get('Код', '').strip()
            name = row.get('Група професій', '').strip()

            if not code or not name:
                continue

            if '.' in code:
                continue

            level = get_code_level(code)
            if not level or level == 'position':
                continue

            try:
                if level == 'section':
                    Section.objects.get_or_create(
                        code=code,
                        defaults={'name': name}
                    )
                    stats['sections'] += 1

                elif level == 'subsection':
                    parent_code = get_parent_code(code, level)
                    if parent_code:
                        section = Section.objects.filter(code=parent_code).first()
                        if section:
                            Subsection.objects.get_or_create(
                                code=code,
                                defaults={'name': name, 'section': section}
                            )
                            stats['subsections'] += 1
                        else:
                            self.stdout.write(self.style.WARNING(f'Section not found for code {code}, parent: {parent_code}'))
                            stats['errors'] += 1
                    else:
                        self.stdout.write(self.style.WARNING(f'Could not determine parent for subsection {code}'))
                        stats['errors'] += 1

                elif level == 'class':
                    parent_code = get_parent_code(code, level)
                    subsection = None
                    section = None

                    if parent_code:
                        subsection = Subsection.objects.filter(code=parent_code).first()
                        if not subsection:
                            section_code = get_parent_code(parent_code, 'subsection')
                            if section_code:
                                section = Section.objects.filter(code=section_code).first()

                    if subsection:
                        Class.objects.get_or_create(
                            code=code,
                            defaults={'name': name, 'subsection': subsection, 'section': subsection.section}
                        )
                        stats['classes'] += 1
                    elif section:
                        Class.objects.get_or_create(
                            code=code,
                            defaults={'name': name, 'subsection': None, 'section': section}
                        )
                        stats['classes'] += 1
                    else:
                        self.stdout.write(self.style.WARNING(f'Parent not found for class {code}, parent code: {parent_code}'))
                        stats['errors'] += 1

                elif level == 'subclass':
                    parent_code = get_parent_code(code, level)
                    if parent_code:
                        class_obj = Class.objects.filter(code=parent_code).first()
                        if class_obj:
                            Subclass.objects.get_or_create(
                                code=code,
                                defaults={'name': name, 'class_obj': class_obj}
                            )
                            stats['subclasses'] += 1
                        else:
                            self.stdout.write(self.style.WARNING(f'Class not found for subclass {code}, parent: {parent_code}'))
                            stats['errors'] += 1
                    else:
                        self.stdout.write(self.style.WARNING(f'Could not determine parent for subclass {code}'))
                        stats['errors'] += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error processing {code} ({name}): {e}'))
                stats['errors'] += 1

        # Second pass: Import Positions and handle Groups
        # A 4-digit Subclass that has Position children should be converted to a Group
        self.stdout.write('Pass 2: Importing positions and creating groups...')
        position_parents = {}  # Track which 4-digit codes have positions

        for idx, row in enumerate(rows, 1):
            if idx % 100 == 0:
                self.stdout.write(f'Processing row {idx}/{total_rows}...')

            code = row.get('Код', '').strip()
            name = row.get('Група професій', '').strip()

            if not code or not name:
                continue

            if '.' not in code:
                continue

            level = get_code_level(code)
            if level != 'position':
                continue

            try:
                parent_code = get_parent_code(code, level)
                if parent_code:
                    position_parents[parent_code] = True

                    group = Group.objects.filter(code=parent_code).first()
                    subclass = None

                    if not group:
                        subclass = Subclass.objects.filter(code=parent_code).first()
                        if subclass:
                            # Convert Subclass to Group (Subclass with Position children becomes Group)
                            group, created = Group.objects.get_or_create(
                                code=parent_code,
                                defaults={'name': subclass.name, 'class_obj': subclass.class_obj}
                            )
                            if created:
                                stats['groups'] += 1
                                stats['subclasses'] -= 1
                                # Delete the Subclass since it's now a Group
                                subclass.delete()

                    if group:
                        Position.objects.get_or_create(
                            code=code,
                            name=name,
                            group=group
                        )
                        stats['positions'] += 1
                    else:
                        self.stdout.write(self.style.WARNING(f'Parent not found for position {code}, parent code: {parent_code}'))
                        stats['errors'] += 1
                else:
                    self.stdout.write(self.style.WARNING(f'Could not determine parent for position {code}'))
                    stats['errors'] += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error processing {code} ({name}): {e}'))
                stats['errors'] += 1

        self.stdout.write(self.style.SUCCESS('\nImport completed!'))
        self.stdout.write(f'Sections: {stats["sections"]}')
        self.stdout.write(f'Subsections: {stats["subsections"]}')
        self.stdout.write(f'Classes: {stats["classes"]}')
        self.stdout.write(f'Subclasses: {stats["subclasses"]}')
        self.stdout.write(f'Groups: {stats["groups"]}')
        self.stdout.write(f'Positions: {stats["positions"]}')
        if stats['errors'] > 0:
            self.stdout.write(self.style.WARNING(f'Errors: {stats["errors"]}'))

