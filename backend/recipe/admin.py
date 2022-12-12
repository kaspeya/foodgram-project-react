from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (FavoriteRecipe, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)

admin.site.site_header = 'Администрирование Foodgram'
EMPTY_VALUE_DISPLAY = 'Значение не указано'


class IngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 10


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    save_on_top = True
    empty_value_display = EMPTY_VALUE_DISPLAY
    list_display = ('id', 'name', 'hex_color_code', 'slug')
    search_fields = ('id', 'name', 'hex_color_code', 'slug')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    save_on_top = True
    empty_value_display = EMPTY_VALUE_DISPLAY
    list_display = ('id', 'name', 'measurement_unit',)
    search_fields = ('id', 'name',)
    list_filter = ('name',)
    fields = ('name', 'measurement_unit',)


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    empty_value_display = EMPTY_VALUE_DISPLAY
    list_display = (
        'id', 'recipe', 'ingredient', 'amount')
    search_fields = (
        'id', 'recipe', 'ingredient'
    )
    list_filter = (
        'id', 'recipe', 'ingredient'
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    save_on_top = True
    empty_value_display = EMPTY_VALUE_DISPLAY
    list_display = (
        'id', 'get_author', 'name', 'text',
        'cooking_time', 'get_tags', 'get_ingredient',
        'pub_date', 'get_favorite_count')
    search_fields = (
        'name', 'cooking_time',
        'author__email', 'ingredient__name')
    list_filter = ('pub_date', 'tags',)
    list_filter = ('name', 'tags', 'author__username')
    fields = (
        ('name', 'cooking_time',),
        ('author', 'tags',),
        ('text',),
        ('image',),
    )
    inlines = (IngredientInline,)

    @admin.display(
        description='автор')
    def get_author(self, obj):
        return obj.author.username

    @admin.display(description='Тэги')
    def get_tags(self, obj):
        list_ = [_.name for _ in obj.tags.all()]
        return ', '.join(list_)

    @admin.display(description=' Ингредиенты ')
    def get_ingredient(self, obj):
        return '\n '.join([
            f'{item["ingredient__name"]} - {item["amount"]}'
            f' {item["ingredient__measurement_unit"]}.'
            for item in obj.recipe.values(
                'ingredient__name',
                'amount', 'ingredient__measurement_unit')])

    @admin.display(description='В избранном')
    def get_favorite_count(self, obj):
        return obj.favorite_recipe.count()

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="80" hieght="30"')

    get_image.short_description = 'Изображение'


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    empty_value_display = EMPTY_VALUE_DISPLAY
    list_display = (
        'id', 'user',)


@admin.register(ShoppingCart)
class SoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user',)
    empty_value_display = EMPTY_VALUE_DISPLAY
