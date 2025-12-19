import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from location.models import Region, District, Community, Settlement, CityDistrict

class Command(BaseCommand):
    help = 'Load CATOTTG data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file', 
            type=str, 
            default='temp/kodifikator.csv',
            help='Path to the CATOTTG CSV file'
        )

    def handle(self, *args, **options):
        file_path = options['file']
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return

        self.stdout.write(f'Loading data from {file_path}...')

        # We will do multiple passes to ensure parents exist
        # Pass 1: Regions (O, K)
        # Pass 2: Districts (P)
        # Pass 3: Communities (H)
        # Pass 4: Settlements (M, T, C, X)
        # Pass 5: City Districts (B)
        
        categories_order = [
            ['O', 'K'], # Regions
            ['P'],      # Districts
            ['H'],      # Communities
            ['M', 'T', 'C', 'X'], # Settlements
            ['B']       # City Districts
        ]

        total_created = 0

        # Read all rows into memory to avoid opening file multiple times (file is ~3MB, usually fine)
        # If file is huge, we would loop file multiple times. 3MB is tiny.
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=';')
            rows = list(reader)

        for pass_cats in categories_order:
            self.stdout.write(f'Processing categories: {pass_cats}...')
            count = 0
            for row in rows:
                cat = row["Категорія об’єкта"]
                if cat not in pass_cats:
                    continue
                
                name = row["Назва об’єкта"]
                
                # CATOTTG CSV Headers:
                # Перший рівень;Другий рівень;Третій рівень;Четвертий рівень;Додатковий рівень;Категорія об’єкта;Назва об’єкта
                
                # Check level based on category to find current code and parent
                try:
                    if cat in ['O', 'K']: # Region
                        code = row["Перший рівень"]
                        Region.objects.get_or_create(
                            code=code,
                            defaults={'name': name, 'category': cat}
                        )
                    
                    elif cat == 'P': # District
                        code = row["Другий рівень"]
                        parent_code = row["Перший рівень"]
                        parent = Region.objects.filter(code=parent_code).first()
                        if parent:
                            District.objects.get_or_create(
                                code=code,
                                defaults={'name': name, 'region': parent}
                            )
                    
                    elif cat == 'H': # Community
                        code = row["Третій рівень"]
                        parent_code = row["Другий рівень"]
                        # Sometimes Communities are direct children of Regions? (unlikely in new reform, but check)
                        # Actually in new reform: Region -> District -> Community.
                        parent = District.objects.filter(code=parent_code).first()
                        if parent:
                            Community.objects.get_or_create(
                                code=code,
                                defaults={'name': name, 'district': parent}
                            )
                    
                    elif cat in ['M', 'T', 'C', 'X']: # Settlement
                        code = row["Четвертий рівень"]
                        parent_code = row["Третій рівень"]
                        parent = Community.objects.filter(code=parent_code).first()
                        if parent:
                            Settlement.objects.get_or_create(
                                code=code,
                                defaults={'name': name, 'category': cat, 'community': parent}
                            )
                    
                    elif cat == 'B': # City District
                        code = row["Додатковий рівень"]
                        parent_code = row["Четвертий рівень"]
                        parent = Settlement.objects.filter(code=parent_code).first()
                        if parent:
                            CityDistrict.objects.get_or_create(
                                code=code,
                                defaults={'name': name, 'settlement': parent}
                            )
                    
                    count += 1
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'Error processing {name} ({cat}): {e}'))

            self.stdout.write(self.style.SUCCESS(f'Processed {count} items for categories {pass_cats}'))
            total_created += count

        self.stdout.write(self.style.SUCCESS(f'Successfully finished. processed {total_created} items.'))
