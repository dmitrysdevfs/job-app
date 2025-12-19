import csv
import os
from django.core.management.base import BaseCommand
from kved.models import Section, Division, Group, Class

class Command(BaseCommand):
    help = 'Load KVED-2010 data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='temp/dc_009_2010_1.csv',
            help='Path to the KVED CSV file'
        )

    def handle(self, *args, **options):
        file_path = options['file']
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return

        self.stdout.write(f'Loading data from {file_path}...')

        stats = {
            'sections': 0,
            'divisions': 0,
            'groups': 0,
            'classes': 0,
            'errors': 0
        }

        with open(file_path, 'r', encoding='utf-8-sig') as f:
            # First, read the header line to normalize it
            header_line = f.readline()
            # Split by semicolon and strip quotes and whitespace from each column name
            fieldnames = [c.strip().strip('"').strip() for c in header_line.split(';')]
            
            reader = csv.DictReader(f, fieldnames=fieldnames, delimiter=';')
            
            # Since we consumed the header line manually, DictReader might treat the first data row as correct.
            # But wait, DictReader usually takes f. If I provide fieldnames, it treats all subsequent lines as data.
            # If I don't provide fieldnames, it reads the first line as header.
            # The header in the file has newlines inside quotes. standard csv module handles that if configured right.
            # Let's try standard approach with stripping keys.

        # Re-open to be safe and simple
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=';')
            # Normalize keys: strip whitespace from keys
            # We can't easily change keys in DictReader in-flight efficiently without reading all.
            # So let's just be careful with key access.
            
            # Actually, let's map the specific keys we expect by checking what they start with.
            # Or better, just strip mapped keys for every row.
            
            normalized_rows = []
            for row in reader:
                clean_row = {k.strip().replace('\n', ''): v for k, v in row.items() if k}
                normalized_rows.append(clean_row)

        total_rows = len(normalized_rows)
        self.stdout.write(f'Processing {total_rows} rows...')

        for idx, row in enumerate(normalized_rows, 1):
            if idx % 100 == 0:
                self.stdout.write(f'Processing row {idx}/{total_rows}...')

            name = row.get('Назва', '').strip()
            
            # Code fields
            code_section = row.get('Код секції', '').strip()
            code_division = row.get('Код розділу', '').strip()
            code_group = row.get('Код групи', '').strip()
            code_class = row.get('Код класу', '').strip()

            try:
                # Logic: check from most specific to least specific, but we need parents to exist.
                # Actually, the file structure usually has parent rows before child rows.
                # Let's assume the file is sorted or we handle missing parents (which might fail if unsorted).
                # But typically KVED files are sorted: Section A, then Division 01, then Group 01.1, then Class 01.11.

                if code_class:
                    # It's a Class
                    # Parent Group should exist (code_group)
                    group = Group.objects.filter(code=code_group).first()
                    if group:
                        Class.objects.get_or_create(
                            code=code_class,
                            defaults={'name': name, 'group': group}
                        )
                        stats['classes'] += 1
                    else:
                        self.stdout.write(self.style.WARNING(f'Parent Group {code_group} not found for Class {code_class}'))
                        stats['errors'] += 1

                elif code_group:
                    # It's a Group
                    # Parent Division should exist (code_division)
                    division = Division.objects.filter(code=code_division).first()
                    if division:
                        Group.objects.get_or_create(
                            code=code_group,
                            defaults={'name': name, 'division': division}
                        )
                        stats['groups'] += 1
                    else:
                        self.stdout.write(self.style.WARNING(f'Parent Division {code_division} not found for Group {code_group}'))
                        stats['errors'] += 1

                elif code_division:
                    # It's a Division
                    # Parent Section should exist (code_section)
                    section = Section.objects.filter(code=code_section).first()
                    if section:
                        Division.objects.get_or_create(
                            code=code_division,
                            defaults={'name': name, 'section': section}
                        )
                        stats['divisions'] += 1
                    else:
                        # Sometimes Section code might be missing in the row?
                        # In the user preview: "A;01;;;..." -> Section A is in the row.
                        self.stdout.write(self.style.WARNING(f'Parent Section {code_section} not found for Division {code_division}'))
                        stats['errors'] += 1

                elif code_section:
                    # It's a Section
                    Section.objects.get_or_create(
                        code=code_section,
                        defaults={'name': name}
                    )
                    stats['sections'] += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error row {idx}: {e}'))
                stats['errors'] += 1

        self.stdout.write(self.style.SUCCESS('\nImport completed!'))
        self.stdout.write(f"Sections: {stats['sections']}")
        self.stdout.write(f"Divisions: {stats['divisions']}")
        self.stdout.write(f"Groups: {stats['groups']}")
        self.stdout.write(f"Classes: {stats['classes']}")
        if stats['errors'] > 0:
            self.stdout.write(self.style.WARNING(f"Errors: {stats['errors']}"))
