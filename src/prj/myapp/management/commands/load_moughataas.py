from django.core.management.base import BaseCommand, CommandError
from myapp.models import Wilaya, Moughataa
import json

class Command(BaseCommand):
    help = 'Load Moughataa data from Communes GeoJSON'

    def add_arguments(self, parser):
        parser.add_argument('--communes', type=str, help='Path to communes GeoJSON file')

    def handle(self, *args, **options):
        if options['communes']:
            try:
                with open(options['communes'], 'r', encoding='utf-8') as f:
                    communes_data = json.load(f)
                    for feature in communes_data['features']:
                        commune_code = feature['properties']['code']

                        # Extract Moughataa and Wilaya code from Commune code
                        moughataa_code = commune_code[:5]
                        wilaya_code = commune_code[:3]
                        
                        moughataa_name = feature['properties']['name']

                        # Get the associated Wilaya
                        try:
                            wilaya = Wilaya.objects.get(code=wilaya_code)
                        except Wilaya.DoesNotExist:
                            self.stdout.write(self.style.WARNING(f'Wilaya not found: {wilaya_code} for commune {commune_name}'))
                            continue

                        # Create or update the Moughataa object
                        moughataa, created = Moughataa.objects.get_or_create(
                            code=moughataa_code,
                            defaults={
                                'name': moughataa_name,
                                'wilaya': wilaya
                            }
                        )
                        if created:
                            self.stdout.write(self.style.SUCCESS(f'Created Moughataa: {moughataa.name}'))
                        else:
                            self.stdout.write(self.style.SUCCESS(f'Updated Moughataa: {moughataa.name}'))

            except FileNotFoundError:
                raise CommandError(f"Communes GeoJSON file not found: {options['communes']}")
        else:
            raise CommandError("Please provide the path to the communes GeoJSON file using --communes")