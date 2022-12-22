from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from users.serializers import UserSerializer

from .models import Ingredient, Recipe, RecipeIngredient, Tag

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all())
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(
        source='recipeingredients',
        many=True,
        read_only=True,
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def get_is_favorited(self, recipe):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(
            favorites__user=user, id=recipe.id).exists()

    def get_is_in_shopping_cart(self, recipe):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(
            cart__user=user, id=recipe.id).exists()

    def create_recipe_ingredients(self, ingredients, recipe):
        recipe_ingredients = []
        for ingredient in ingredients:
            recipe_ingredient = RecipeIngredient(
                recipe=recipe,
                ingredient_id=ingredient['ingredient']['id'],
                amount=ingredient['amount']
            )
            recipe_ingredients.append(recipe_ingredient)

        RecipeIngredient.objects.bulk_create(recipe_ingredients)

    def create_recipe(self, validated_data):
        image = validated_data.pop('image')
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('recipeingredients')
        recipe = Recipe.objects.bulk_create(image=image, **validated_data)
        recipe.tags.set(tags)
        self.create_recipe_ingredients(recipe, ingredients)
        return recipe

    def update_recipe(self, recipe, validated_data):
        recipe.image = validated_data.get('image', recipe.image)
        recipe.name = validated_data.get('name', recipe.name)
        recipe.text = validated_data.get('text', recipe.text)
        recipe.cooking_time = validated_data.get(
            'cooking_time', recipe.cooking_time)
        tags = validated_data.get('tags')
        if tags:
            recipe.tags.clear()
            recipe.tags.set(tags)

        ingredients = validated_data.pop('recipeingredients')
        recipe.ingredients.clear()
        self.create_recipe_ingredients(ingredients, recipe)
        recipe.save()
        return recipe
