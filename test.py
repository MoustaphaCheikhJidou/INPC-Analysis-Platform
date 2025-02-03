from django.core.management.base import BaseCommand
from prj.myapp.models import Wilaya, Moughataa, Commune
from django.db import transaction

class Command(BaseCommand):
    def handle(self, *args, **options):
        # First, create Moughataa records
        moughataa_data = {
            'MR211': {'name': 'Barkéol', 'wilaya_code': 'MR21'},
            'MR221': {'name': 'Boumdeïd', 'wilaya_code': 'MR22'},
            'MR231': {'name': 'Guérou', 'wilaya_code': 'MR23'},
            'MR241': {'name': 'Kankossa', 'wilaya_code': 'MR24'},
            'MR251': {'name': 'Kiffa', 'wilaya_code': 'MR25'},
            'MR311': {'name': 'Aleg', 'wilaya_code': 'MR31'},
            'MR321': {'name': 'Bababé', 'wilaya_code': 'MR32'},
            'MR331': {'name': 'Boghé', 'wilaya_code': 'MR33'},
            'MR341': {'name': "M'Bagne", 'wilaya_code': 'MR34'},
            'MR351': {'name': 'Magta-Lahjar', 'wilaya_code': 'MR35'},
            'MR411': {'name': 'Nouadhibou', 'wilaya_code': 'MR41'},
            'MR511': {'name': 'Kaédi', 'wilaya_code': 'MR51'},
            'MR521': {'name': "M'Bout", 'wilaya_code': 'MR52'},
            'MR531': {'name': 'Maghama', 'wilaya_code': 'MR53'},
            'MR541': {'name': 'Monguel', 'wilaya_code': 'MR54'},
            'MR611': {'name': 'OuldYengé', 'wilaya_code': 'MR61'},
            'MR621': {'name': 'Sélibaby', 'wilaya_code': 'MR62'},
            'MR711': {'name': 'Amourj', 'wilaya_code': 'MR71'},
            'MR721': {'name': 'Bassikounou', 'wilaya_code': 'MR72'},
            'MR731': {'name': 'Djiguenni', 'wilaya_code': 'MR73'},
            'MR741': {'name': 'Néma', 'wilaya_code': 'MR74'},
            'MR751': {'name': 'Ouadane', 'wilaya_code': 'MR75'},
            'MR761': {'name': 'Timbédra', 'wilaya_code': 'MR76'},
            'MR811': {'name': 'Aïoun', 'wilaya_code': 'MR81'},
            'MR821': {'name': 'Kobenni', 'wilaya_code': 'MR82'},
            'MR831': {'name': 'Tamchakett', 'wilaya_code': 'MR83'},
            'MR841': {'name': 'Tintane', 'wilaya_code': 'MR84'},
            'MR911': {'name': 'Akjoujt', 'wilaya_code': 'MR91'},
            'MR123': {'name': 'Zouérate', 'wilaya_code': 'MR12'},
            'MR134': {'name': 'Ouad-Naga', 'wilaya_code': 'MR13'},
            'MR135': {'name': "R'Kiz", 'wilaya_code': 'MR13'},
            'MR136': {'name': 'Rosso', 'wilaya_code': 'MR13'},
        }

        with transaction.atomic():
            for code, data in moughataa_data.items():
                try:
                    wilaya = Wilaya.objects.get(code=data['wilaya_code'])
                    Moughataa.objects.get_or_create(
                        code=code,
                        defaults={
                            'name': data['name'],
                            'wilaya': wilaya
                        }
                    )
                    self.stdout.write(f"Created/Updated Moughataa: {data['name']}")
                except Wilaya.DoesNotExist:
                    self.stdout.write(f"Wilaya not found for code: {data['wilaya_code']}")