import csv
import logging
from django.core.management.base import BaseCommand
from django.db import transaction
from speciality.models import KnowledgeField, Speciality

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Import Knowledge Fields and Specialities from CSV'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, nargs='?', default='temp/speciality.csv', help='Path to the CSV file')

    def handle(self, *args, **options):
        file_path = options['file_path']
        self.stdout.write(f"Starting import from {file_path}...")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=';')
                header = next(reader, None)  # Skip header

                with transaction.atomic():
                    self.process_rows(reader)
            
            self.stdout.write(self.style.SUCCESS("Import completed successfully"))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))
            logger.exception("Import failed")

    def process_rows(self, reader):
        count_kf = 0
        count_spec = 0

        for row_num, row in enumerate(reader, start=2):
            if not row or len(row) < 2:
                continue

            field_raw = row[0].strip()
            spec_raw = row[1].strip()

            # Process Knowledge Field if present
            if field_raw:
                # Expecting format "01 Name", split by first space
                parts = field_raw.split(' ', 1)
                if len(parts) == 2:
                    code, name = parts
                    KnowledgeField.objects.get_or_create(
                        code=code,
                        defaults={'name': name}
                    )
                    count_kf += 1

            # Process Speciality if present
            if spec_raw:
                # Expecting format "011 Name", split by first space
                parts = spec_raw.split(' ', 1)
                if len(parts) == 2:
                    code, name = parts
                    
                    # Logic: Link to KnowledgeField via first 2 digits of speciality code
                    kf_code = code[:2]
                    
                    try:
                        kf = KnowledgeField.objects.get(code=kf_code)
                        Speciality.objects.get_or_create(
                            code=code,
                            defaults={
                                'name': name,
                                'knowledge_field': kf,
                                'level': 1,  # Flat list for now
                                'parent': None
                            }
                        )
                        count_spec += 1
                    except KnowledgeField.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f"Row {row_num}: KnowledgeField {kf_code} not found for Speciality {code}. Skipping."))

        self.stdout.write(f"Processed: {count_kf} Knowledge Fields, {count_spec} Specialities")
