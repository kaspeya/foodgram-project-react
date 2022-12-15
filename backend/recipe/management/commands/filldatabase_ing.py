import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from recipe.models import Ingredient


class Command(BaseCommand):
    help = "'Import from `../data/ingredients.json'`"

    def handle(self, *args, **options):
        with open(os.path.join(settings.BASE_DIR, 'data/ingredients.json'),
                  encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)
            for row in data:
                Ingredient.objects.get_or_create(
                    name=row['name'],
                    measurement_unit=row['measurement_unit'])
        self.stdout.write(self.style.SUCCESS('Ингридиенты загружены!'))
