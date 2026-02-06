import csv
from django.core.management.base import BaseCommand
from eonapp.models import Bird

class Command(BaseCommand):
    help = 'Import birds from birds.csv into the database'

    def handle(self, *args, **kwargs):
        count = 0

        with open('Birds CSV 05.csv', newline='', encoding='latin1', errors='ignore') as file:
            reader = csv.DictReader(file)

            for row in reader:
                clean_row = {}

                for k, v in row.items():
                    key = (
                        k.strip()
                         .replace(' ', '_')
                         .replace('\ufeff', '')
                    )

                    if key == 'Bird_Sub_SpeciesDetails':
                        key = 'Bird_Sub_Species_Details'

                    if isinstance(v, str):
                        v = v.replace('\r\n', '\n').replace('\r', '\n')

                    clean_row[key] = v

                bird = Bird.objects.create(**clean_row)
                bird.save()  # 🔥 Triggers slug generation from Bird_Name
                count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} birds ✅'))
