from django.core.management import BaseCommand
from recipe.models import Tag


class Command(BaseCommand):
    help = 'Fills the database'

    def handle(self, *args, **kwargs):
        data = [
            {
                'name': 'Завтрак',
                'hex_color_code': '#E26C2D',
                'slug': 'breakfast'
            },
            {
                'name': 'Обед',
                'hex_color_code': '#49B64E',
                'slug': 'dinner'
            },
            {
                'name': 'Ужин',
                'hex_color_code': '#8775D2',
                'slug': 'supper'
            }
        ]
        Tag.objects.bulk_create(Tag(**tag) for tag in data)
        self.stdout.write(self.style.SUCCESS('Теги загружены!'))
