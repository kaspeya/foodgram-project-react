from django.contrib.auth import get_user_model
from django.db.models.aggregates import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .filters import IngredientFilter, RecipesFilter
from .models import (FavoriteRecipe, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)
from .pagination import LimitPageNumberPagination
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer
from .utils import generate_report

User = get_user_model()


class TagsViewSet(ReadOnlyModelViewSet):
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(ReadOnlyModelViewSet):
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    search_fields = ('^name',)
    filter_backends = (DjangoFilterBackend, IngredientFilter)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipesFilter
    pagination_class = LimitPageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite_recipe(self, request, pk=None):
        if request.method == 'GET':
            return self.add_obj(FavoriteRecipe, request.user, pk)
        if request.method == 'DELETE':
            return self.delete_obj(FavoriteRecipe, request.user, pk)
        return None

    @action(detail=True, methods=['get', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        if request.method == 'GET':
            return self.add_obj(ShoppingCart, request.user, pk)
        if request.method == 'DELETE':
            return self.delete_obj(ShoppingCart, request.user, pk)
        return None

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients_list = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(total=Sum('amount'))

        return generate_report(ingredients_list)

    def add_user_recipe_model(self, user, recipe,
                              model_class, serializer_class):
        if model_class.objects.filter(user=user, recipe=recipe).exists():
            return Response({'errors': 'Этот рецепт уже добавлен в список.'},
                            status=status.HTTP_400_BAD_REQUEST)
        model = model_class.objects.create(user=user, recipe=recipe)
        serializer = serializer_class(model)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_user_recipe_model(self, user, recipe, model_class):
        model = model_class.objects.filter(user=user, recipe=recipe)
        if not model.exists():
            return Response({"error": 'Рецепт уже удален.'},
                            status=status.HTTP_400_BAD_REQUEST)

        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
