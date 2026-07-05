from django.core.management.base import BaseCommand
from django.utils.text import slugify
from content.models import Category


class Command(BaseCommand):
    help = 'Seed default Umbrella content categories.'

    def handle(self, *args, **options):
        categories = [
            'Movies', 'TV Series', 'Documentaries', 'Education', 'Comedy',
            'Music', 'Drama', 'Sports', 'Kids', 'Religion', 'News', 'Culture'
        ]
        for name in categories:
            Category.objects.update_or_create(slug=slugify(name), defaults={'name': name, 'is_active': True})
        self.stdout.write(self.style.SUCCESS('Default categories seeded.'))
