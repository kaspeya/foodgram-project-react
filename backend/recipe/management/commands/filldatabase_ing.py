import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from recipe.models import Ingredient


class Command(BaseCommand):
    help = "Import from `../data/ingredients.csv`"

    def handle(self, *args, **kwargs):
        with open(os.path.join(settings.BASE_DIR, 'data/ingredients.csv'),
                  encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)
            for row in csvreader:
                Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1],
                )
        self.stdout.write(self.style.SUCCESS('Ингридиенты загружены!'))
