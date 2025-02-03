import json
import os
from django.core.management.base import BaseCommand, CommandError
from myapp.models import Wilaya, Moughataa, Commune

class Command(BaseCommand):
    help = 'Load GeoJSON data for Wilayas, Communes, and Moughataas.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--wilayas',
            type=str,
            help='Path to the Wilayas GeoJSON file'
        )
        parser.add_argument(
            '--communes',
            type=str,
            help='Path to the Communes GeoJSON file'
        )
        parser.add_argument(
            '--moughataas',
            type=str,
            help='Path to the Moughataas GeoJSON file'
        )

    def handle(self, *args, **options):
        # Process Moughataas file if provided.
        m_file = options.get('moughataas')
        if m_file:
            abs_path = os.path.abspath(m_file)
            self.stdout.write(f"Loading Moughataas GeoJSON from: {abs_path}")
            if not os.path.exists(abs_path):
                raise CommandError(f"File not found: {abs_path}")
            try:
                with open(abs_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception as e:
                raise CommandError(f"Error loading Moughataas file: {e}")
            features = data.get("features", [])
            if not features:
                self.stdout.write("No features found in the Moughataas file.")
            else:
                updated_count = 0
                for feature in features:
                    properties = feature.get("properties", {})
                    # Use fallback keys for the unique identifier and name.
                    code = properties.get("code") or properties.get("GID_2")
                    name = properties.get("name") or properties.get("NAME_2") or properties.get("NAME_1")
                    geometry = feature.get("geometry")
                    self.stdout.write(f"Feature properties: {properties}")
                    if not (code and geometry):
                        self.stdout.write(f"Skipping feature with missing code or geometry: {feature}")
                        continue

                    # *** NEW: Determine the wilaya using the GeoJSON property ***
                    # For example, we assume the property "GID_1" holds the wilaya code.
                    wilaya_code = properties.get("GID_1")
                    if not wilaya_code:
                        self.stdout.write(f"Skipping feature {code} because no wilaya code was found in its properties.")
                        continue
                    try:
                        wilaya = Wilaya.objects.get(code=wilaya_code)
                    except Wilaya.DoesNotExist:
                        self.stdout.write(f"Wilaya with code '{wilaya_code}' not found for moughataa {code}. Skipping this feature.")
                        continue

                    try:
                        geometry_json = json.dumps(geometry)
                        moughataa, created = Moughataa.objects.update_or_create(
                            code=code,
                            defaults={
                                'name': name,
                                'polygon': geometry_json,
                                'wilaya': wilaya,
                            }
                        )
                        if created:
                            self.stdout.write(self.style.SUCCESS(f"Created Moughataa: {moughataa.name} (code: {code})"))
                        else:
                            self.stdout.write(self.style.SUCCESS(f"Updated Moughataa: {moughataa.name} (code: {code})"))
                        updated_count += 1
                    except Exception as e:
                        self.stderr.write(f"Error updating Moughataa with code {code}: {e}")
                self.stdout.write(self.style.SUCCESS(f"Updated {updated_count} moughataa polygons."))

        # (You can similarly process the --wilayas and --communes files.)
        if options.get('wilayas'):
            abs_path = os.path.abspath(options['wilayas'])
            self.stdout.write(f"Loading Wilayas GeoJSON from: {abs_path}")
            if not os.path.exists(abs_path):
                raise CommandError(f"Wilayas file not found: {abs_path}")
            try:
                with open(abs_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception as e:
                raise CommandError(f"Error loading Wilayas file: {e}")
            features = data.get("features", [])
            if not features:
                self.stdout.write("No features found in the Wilayas file.")
            else:
                updated_count = 0
                for feature in features:
                    properties = feature.get("properties", {})
                    code = properties.get("code") or properties.get("GID_1")
                    name = properties.get("name") or properties.get("NAME_1")
                    geometry = feature.get("geometry")
                    if not (code and geometry):
                        self.stdout.write(f"Skipping feature with missing code or geometry: {feature}")
                        continue
                    try:
                        geometry_json = json.dumps(geometry)
                        wilaya, created = Wilaya.objects.update_or_create(
                            code=code,
                            defaults={'name': name, 'polygon': geometry_json}
                        )
                        if created:
                            self.stdout.write(self.style.SUCCESS(f"Created Wilaya: {wilaya.name} (code: {code})"))
                        else:
                            self.stdout.write(self.style.SUCCESS(f"Updated Wilaya: {wilaya.name} (code: {code})"))
                        updated_count += 1
                    except Exception as e:
                        self.stderr.write(f"Error updating Wilaya with code {code}: {e}")
                self.stdout.write(self.style.SUCCESS(f"Updated {updated_count} wilaya polygons."))

        if options.get('communes'):
            abs_path = os.path.abspath(options['communes'])
            self.stdout.write(f"Loading Communes GeoJSON from: {abs_path}")
            if not os.path.exists(abs_path):
                raise CommandError(f"Communes file not found: {abs_path}")
            try:
                with open(abs_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception as e:
                raise CommandError(f"Error loading Communes file: {e}")
            features = data.get("features", [])
            if not features:
                self.stdout.write("No features found in the Communes file.")
            else:
                updated_count = 0
                for feature in features:
                    properties = feature.get("properties", {})
                    code = properties.get("code") or properties.get("GID_2")
                    name = properties.get("name") or properties.get("NAME_2")
                    geometry = feature.get("geometry")
                    if not (code and geometry):
                        self.stdout.write(f"Skipping feature with missing code or geometry: {feature}")
                        continue
                    try:
                        geometry_json = json.dumps(geometry)
                        commune, created = Commune.objects.update_or_create(
                            code=code,
                            defaults={'name': name, 'polygon': geometry_json}
                        )
                        if created:
                            self.stdout.write(self.style.SUCCESS(f"Created Commune: {commune.name} (code: {code})"))
                        else:
                            self.stdout.write(self.style.SUCCESS(f"Updated Commune: {commune.name} (code: {code})"))
                        updated_count += 1
                    except Exception as e:
                        self.stderr.write(f"Error updating Commune with code {code}: {e}")
                self.stdout.write(self.style.SUCCESS(f"Updated {updated_count} commune polygons."))

        self.stdout.write(self.style.SUCCESS("GeoJSON data loaded successfully."))
