from django.core.management.base import BaseCommand
from subscriptions.models import Plan


class Command(BaseCommand):
    help = 'Seed default Umbrella subscription plans.'

    def handle(self, *args, **options):
        plans = [
            {
                'code': 'basic', 'name': 'Basic Plan', 'price_tzs': 5000,
                'description': 'Affordable mobile-first access.', 'max_devices': 1,
                'max_quality': '720p', 'downloads_enabled': False,
                'early_access_enabled': False, 'monthly_award_points': 10,
            },
            {
                'code': 'standard', 'name': 'Standard Plan', 'price_tzs': 10000,
                'description': 'HD streaming and more monthly creator award points.', 'max_devices': 2,
                'max_quality': '1080p', 'downloads_enabled': True,
                'early_access_enabled': False, 'monthly_award_points': 25,
            },
            {
                'code': 'premium', 'name': 'Premium Plan', 'price_tzs': 20000,
                'description': 'Best quality, early access and higher award points.', 'max_devices': 4,
                'max_quality': '4K', 'downloads_enabled': True,
                'early_access_enabled': True, 'monthly_award_points': 50,
            },
        ]
        for item in plans:
            Plan.objects.update_or_create(code=item['code'], defaults=item)
        self.stdout.write(self.style.SUCCESS('Default plans seeded.'))
