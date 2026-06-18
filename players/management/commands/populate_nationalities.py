from django.core.management.base import BaseCommand
from players.models import Nationality
from players.countries import COUNTRIES


class Command(BaseCommand):
    help = 'Populate the Nationality model with all countries'

    def handle(self, *args, **options):
        created_count = 0
        existing_count = 0

        for country_code, country_name in COUNTRIES:
            nationality, created = Nationality.objects.get_or_create(name=country_name)
            
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {country_name}'))
            else:
                existing_count += 1

        self.stdout.write(self.style.SUCCESS(f'\n✅ Summary:'))
        self.stdout.write(self.style.SUCCESS(f'   - Created: {created_count} nationalities'))
        self.stdout.write(self.style.SUCCESS(f'   - Already existed: {existing_count} nationalities'))
        self.stdout.write(self.style.SUCCESS(f'   - Total: {created_count + existing_count} nationalities'))
