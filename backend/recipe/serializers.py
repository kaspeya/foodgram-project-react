from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.serializers import UserSerializer

from .models import (FavoriteRecipe, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'hex_color_code', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')
        validators = [
            UniqueTogetherValidator(
                queryset=RecipeIngredient.objects.all(),
                fields=['ingredient', 'recipe']
            )
        ]


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = TagSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(
        source='recipeingredient_set',
        many=True,
        read_only=True,
    )
    is_favorited = serializers.BooleanField(
        read_only=True)
    is_in_shopping_cart = serializers.BooleanField(
        read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def get_is_favorited(self, recipe):
        return self.get_object(FavoriteRecipe, recipe)

    def get_is_in_shopping_cart(self, recipe):
        return self.get_object(ShoppingCart, recipe)

    def get_object(self, model, recipe):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return model.objects.filter(recipe=recipe, user=request.user).exists()


class RecipeCreateSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)
    image = Base64ImageField()
    ingredients = RecipeIngredientSerializer(source='recipeingredients',
                                             many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'image', 'name', 'text', 'cooking_time')

    def validate_ingredients(self, value):
        validated_ingredients = []
        for ingredient in value:
            ingredient_id = ingredient['ingredient']['id']
            if not Ingredient.objects.filter(id=ingredient_id).exists():
                raise serializers.ValidationError(
                    'Данного ингредиента нет в базе!'
                )
            if ingredient_id in validated_ingredients:
                raise serializers.ValidationError(
                    'Данный ингредиент повторяется в рецепте.'
                )
            validated_ingredients.append(ingredient_id)

        for cooking_time in value:
            if not cooking_time or cooking_time < 0:
                raise serializers.ValidationError(
                    'Нужно указать время приготовления рецепта.'
                )
        if not ingredient:
            raise serializers.ValidationError(
                'Нужен хотя бы часть ингридиента для рецепта'
            )
        return value

    def create_ingredients(self, ingredient, recipe):
        RecipeIngredient.objects.bulk_create(
            recipe=recipe,
            ingredient_id=ingredient.get('id'),
            amount=ingredient.get('amount'),
        )

    def create_recipe(self, validated_data):
        image = validated_data.pop('image')
        ingredients_data = validated_data.pop('ingredients', required=True)
        recipe = Recipe.objects.bulk_create(image=image, **validated_data)
        tags_data = self.initial_data.get('tags')
        recipe.tags.set(tags_data)
        self.create_ingredients(ingredients_data, recipe)
        return recipe

    def update_recipe(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.tags.clear()
        tags_data = self.initial_data.get('tags')
        instance.tags.set(tags_data)
        RecipeIngredient.objects.filter(recipe=instance).all().delete()
        self.create_ingredients(validated_data.get('ingredients'), instance)
        instance.save()
        return instance

    def to_representation(self, recipe):
        context = {'request': self.context.get('request')}
        return RecipeSerializer(recipe, context=context).data


class CropRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class CommonFavoriteCartSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        fields = ('user', 'recipe')

    def validate(self, data):
        user = data['user']
        recipe_id = data['recipe'].id
        if self.metaclass.model.objects.filter(
                user=user, recipe__id=recipe_id).exists():
            raise serializers.ValidationError(
                'Рецепт уже добавлен в избранное!')
        return data

    def to_representation(self, instance):
        context = {'request': self.context.get('request')}
        return CropRecipeSerializer(instance.recipe, context=context).data


class FavoriteRecipeSerializer(CommonFavoriteCartSerializer):
    class Meta(CommonFavoriteCartSerializer.Meta):
        model = FavoriteRecipe


class ShoppingCartSerializer(CommonFavoriteCartSerializer):
    class Meta(CommonFavoriteCartSerializer.Meta):
        model = ShoppingCart
