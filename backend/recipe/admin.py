from django.contrib import admin

from .models import (FavoriteRecipe, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)

admin.site.site_header = 'Администрирование Foodgram'
EMPTY_VALUE_DISPLAY = 'Значение не указано'


class IngredientsInline(admin.TabularInline):
    empty_value_display = EMPTY_VALUE_DISPLAY
    model = RecipeIngredient


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    empty_value_display = EMPTY_VALUE_DISPLAY
    list_display = ('id', 'name', 'slug')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    save_on_top = True
    empty_value_display = EMPTY_VALUE_DISPLAY
    list_display = ('id', 'name', 'measurement_unit',)
    search_fields = ('id', 'name',)
    list_filter = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    empty_value_display = EMPTY_VALUE_DISPLAY
    list_display = ('id', 'name', 'author', 'get_favorite_count')
    list_filter = ['name', 'author', 'tags']
    inlines = [IngredientsInline]

    def get_favorite_count(self, obj):
        return obj.favorite_recipes.count()


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    empty_value_display = EMPTY_VALUE_DISPLAY
    list_display = ('id', 'user', 'recipe')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    empty_value_display = EMPTY_VALUE_DISPLAY
    list_display = ('id', 'user', 'recipe')
