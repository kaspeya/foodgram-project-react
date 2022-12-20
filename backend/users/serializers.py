from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from recipe.models import Recipe

from .models import Subscription

User = get_user_model()


class CommonSubscribed(metaclass=serializers.SerializerMetaclass):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    def get_is_subscribed(self, author):
        user = self.context['request'].user
        if user.is_authenticated:
            return Subscription.objects.filter(author=author,
                                               user=user).exists()
        return False


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username',
                  'first_name', 'last_name', 'password')


class UserSerializer(UserSerializer, CommonSubscribed):
    class Meta:
        model = User
        fields = ('id', 'email', 'username',
                  'first_name', 'last_name', 'is_subscribed')


class CropRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionSerializer(serializers.ModelSerializer, CommonSubscribed):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes(self, author):
        recipes_limit = int(
            self.context['request'].GET.get('recipes_limit', 5))
        recipes = Recipe.objects.filter(author=author)[:recipes_limit]

        return CropRecipeSerializer(recipes, many=True).data

    def get_recipes_count(self, author):
        return author.recipes.count()
