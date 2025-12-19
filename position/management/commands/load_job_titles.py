import csv
import os
from django.core.management.base import BaseCommand
from position.models import Position, Group, Subclass, JobTitle

class Command(BaseCommand):
    help = 'Load Job Titles (Detailed) from CSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file', 
            type=str, 
            default='temp/classification_of_professions_details.csv',
            help='Path to the Job Titles CSV file'
        )

    def handle(self, *args, **options):
        file_path = options['file']
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return

        self.stdout.write(f'Loading data from {file_path}...')
        
        # Cache for performance
        # Using codes as keys. Note: Code is not unique for Position, so we store ids as list or first match?
        # Standard says codes are shared by positions in the same group usually. 
        # But for linking, if we have 1120.1, we link to ANY 1120.1 position? 
        # Ideally we match exact one, but if multiple positions have same code (rare but possible now), 
        # we just pick one. For this task, picking first match is acceptable heuristic. 
        
        # However, we just added db_index=True to Position.code, so easy to lookup.
        # caching 1000s of objects might be faster.
        
        count = 0
        errors = 0
        
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f, delimiter=';')
            headers = next(reader, None) # Skip header
            
            # CSV Headers index guess based on inspection:
            # 0: CODE (e.g. "1110 ")
            # 1: ZKPPTR
            # 2: ETKD
            # 3: DKHP
            # 4: NAME
            
            for row in reader:
                if not row or len(row) < 5:
                    continue
                    
                raw_code = row[0].strip()
                # Remove NBSP if any
                raw_code = raw_code.replace('\xa0', '').strip()
                
                if not raw_code or raw_code == "КОД КП":
                    continue
                
                zkpptr = row[1].strip().replace('\xa0', '')
                etkd = row[2].strip().replace('\xa0', '')
                dkhp = row[3].strip().replace('\xa0', '')
                name = row[4].strip().replace('\xa0', '')
                
                if not name:
                    continue
                    
                # Try to find parent
                pos_obj = Position.objects.filter(code=raw_code).first()
                group_obj = None
                subclass_obj = None
                
                if not pos_obj:
                    group_obj = Group.objects.filter(code=raw_code).first()
                    
                if not pos_obj and not group_obj:
                    subclass_obj = Subclass.objects.filter(code=raw_code).first()
                
                # Create JobTitle
                try:
                    JobTitle.objects.update_or_create(
                        code=raw_code,
                        name=name,
                        defaults={
                            'zkpptr_code': zkpptr,
                            'etkd_issue': etkd,
                            'dkhp_issue': dkhp,
                            'position': pos_obj,
                            'group': group_obj,
                            'subclass': subclass_obj
                        }
                    )
                    count += 1
                    if count % 1000 == 0:
                        self.stdout.write(f'Processed {count} records...')
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error creating {name} ({raw_code}): {e}'))
                    errors += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully processed {count} records. Errors: {errors}'))
