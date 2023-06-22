import csv
from decimal import Decimal
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from main_app.models import StaticOnsData  


class Command(BaseCommand):
    help = 'Load data from CSV into the database'

    def handle(self, *args, **options):
        csv_file_path = 'main_app/static_data/rightspot_wide.csv'

        with open(csv_file_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            headers = next(reader)

            model_fields = {name: 'decimal' for name in headers}
            model_fields['district'] = 'char'
            model_fields['date'] = 'int'

            try:
                with transaction.atomic():
                    for row in reader:
                        entry_data = dict(zip(headers, row))

                        # Convert values to the appropriate type.
                        for field_name, field_type in model_fields.items():
                            if field_type == 'decimal':
                                entry_data[field_name] = Decimal(entry_data[field_name])
                            elif field_type == 'int':
                                entry_data[field_name] = int(entry_data[field_name])

                        instance = StaticOnsData(**entry_data)
                        instance.full_clean()
                        instance.save()

            except Exception as e:
                raise CommandError('Failed to load data: %s' % e)

            self.stdout.write(self.style.SUCCESS('Successfully loaded data from "%s"' % csv_file_path))
