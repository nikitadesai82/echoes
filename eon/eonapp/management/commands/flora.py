import csv
from django.core.management.base import BaseCommand
from eonapp.models import Flora

class Command(BaseCommand):
    help = 'Import birds from birds.csv into the database'

    def handle(self, *args, **kwargs):
        count = 0

        with open('Flora CSV 05.csv', encoding='latin1', errors='ignore') as file:
            reader = csv.DictReader(file)

            for row in reader:
                clean_row = {}

                for k, v in row.items():
                    key = (
                        k.strip()
                         .replace(' ', '_')
                         .replace('\ufeff', '')
                    )

                    # Fix wrong column names here
                    if key == 'Bird_Sub_SpeciesDetails':
                        key = 'Bird_Sub_Species_Details'

                    clean_row[key] = v

                Flora.objects.create(**clean_row)
                count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} birds ✅'))