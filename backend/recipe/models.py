from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models
from django.db.models import ManyToManyField

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField('Название ингредиента', max_length=200)
    amount = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name='Количество'
    )
    measurement_unit = models.CharField('Единица измерения', max_length=50)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} {self.measurement_unit}.'


class Tag(models.Model):
    name = models.CharField(
        'Название',
        max_length=200,
        unique=True
    )
    hex_color_code = models.CharField(
        'Цветовой HEX-код',
        max_length=10,
        blank=True,
        null=True,
        default='#49B64E'
    )
    slug = models.SlugField(
        max_length=70,
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['-id']

    def __str__(self):
        return f'{self.name} (цвет: {self.hex_color_code})'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        verbose_name='Название блюда',
        max_length=200,
        unique=True
    )
    image = models.ImageField(
        verbose_name='Изображение блюда',
        upload_to='static/recipe/',
        null=True,
        blank=True
    )
    text = models.TextField('Текстовое описание рецепта')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингридиенты',
        related_name='recipe',
        blank=True
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='recipe',
        verbose_name='Теги'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в минутах',
        validators=[
            validators.MinValueValidator(
                1,
                message='Мин. значение времени приготовления - 1 минута'),
            validators.MaxValueValidator(
                1000,
                message='Макс. допустимое время приготовления - 1000 минут')
        ],
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    favorite = ManyToManyField(
        verbose_name='Понравившиеся рецепты',
        related_name='favorites',
        to=User,
    )
    cart = ManyToManyField(
        verbose_name='Список покупок',
        related_name='carts',
        to=User,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date', )

    def __str__(self) -> str:
        return f'{self.name}. Автор: {self.author.username}'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe')
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингридиент',
    )
    amount = models.PositiveSmallIntegerField(
        default=0,
        validators=(
            validators.MinValueValidator(
                0.5, message='Минимальное количество ингридиентов 0.5'),
            validators.MaxValueValidator(
                10000,
                message='Максимально количество ингридиентов - 100')
        ),
        verbose_name='Количество',)

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        ordering = ['-id']

    def __str__(self):
        return f'{self.amount} {self.ingredient}'


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
        verbose_name='Пользователь')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
        verbose_name='Избранный рецепт')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='Проверка повторного добавления рецепта в избранные',
            )
        ]
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        ordering = ['-id']

    # def __str__(self):
    #     list_ = [item['name'] for item in self.recipe.values('name')]
    #     return f'Пользователь {self.user} добавил {list_} в избранные.'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        null=True,
        verbose_name='Пользователь')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='Проверка повторного добавления рецепта в корзину',
            )
        ]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        ordering = ['-id']

    # def __str__(self):
    #     list_ = [item['name'] for item in self.recipe.values('name')]
    #     return f'Пользователь {self.user} добавил {list_} в список покупок.'
