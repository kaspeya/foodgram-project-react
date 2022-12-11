from django.contrib.admin import (ModelAdmin, TabularInline, display, register,
                                  site)
from django.utils.safestring import mark_safe

from .models import (FavoriteRecipe, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)

site.site_header = 'Администрирование Foodgram'
EMPTY_VALUE_DISPLAY = 'Значение не указано'


class IngredientInline(TabularInline):
    model = RecipeIngredient
    extra = 10


@register(Tag)
class TagAdmin(ModelAdmin):
    save_on_top = True
    empty_value_display = EMPTY_VALUE_DISPLAY
    list_display = (
        'id', 'name', 'hex_color_code', 'slug',
    )
    search_fields = (
        'id', 'name', 'hex_color_code'
    )


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    save_on_top = True
    empty_value_display = EMPTY_VALUE_DISPLAY
    list_display = (
        'id', 'name', 'measurement_unit',)
    search_fields = (
        'id', 'name',)
    list_filter = (
        'id', 'name'
    )


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    save_on_top = True
    empty_value_display = EMPTY_VALUE_DISPLAY
    list_display = (
        'id', 'get_author', 'title', 'text',
        'cooking_time', 'get_tags', 'get_ingredients',
        'pub_date', 'get_favorite_count')
    search_fields = (
        'title', 'cooking_time',
        'author__email', 'ingredients__name')
    list_filter = ('pub_date', 'tag', 'author__username')
    fields = (
        ('title', 'cooking_time',),
        ('author', 'tags',),
        ('text',),
        ('image',),
    )

    inlines = (IngredientInline,)

    @display(
        description='Электронная почта автора')
    def get_author(self, obj):
        return obj.author.email

    @display(description='Тэги')
    def get_tags(self, obj):
        list_ = [tag.name for tag in obj.tags.all()]
        return ', '.join(list_)

    @display(description=' Ингредиенты ')
    def get_ingredients(self, obj):
        return '\n '.join([
            f'{item["ingredient__name"]} - {item["amount"]}'
            f' {item["ingredient__measurement_unit"]}.'
            for item in obj.recipe.values(
                'ingredient__name',
                'amount', 'ingredient__measurement_unit')])

    @display(description='В избранном')
    def get_favorite_count(self, obj):
        return obj.favorite_recipe.count()

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="80" hieght="30"')

    get_image.short_description = 'Изображение'


@register(FavoriteRecipe)
class FavoriteRecipeAdmin(ModelAdmin):
    empty_value_display = EMPTY_VALUE_DISPLAY
    list_display = (
        'id', 'user', 'get_recipe', 'get_count')

    @display(description='Рецепты')
    def get_recipe(self, obj):
        return [
            f'{item["name"]} ' for item in obj.recipe.values('name')[:5]]

    @display(
        description='В избранных')
    def get_count(self, obj):
        return obj.recipe.count()


@register(ShoppingCart)
class SoppingCartAdmin(ModelAdmin):
    list_display = (
        'id', 'user', 'get_recipe', 'get_count')
    empty_value_display = EMPTY_VALUE_DISPLAY

    @display(description='Рецепты')
    def get_recipe(self, obj):
        return [
            f'{item["name"]} ' for item in obj.recipe.values('name')[:5]]

    @display(description='В избранных')
    def get_count(self, obj):
        return obj.recipe.count()
