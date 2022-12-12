from django.db.models.aggregates import Sum
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from recipe.models import (FavoriteRecipe, Ingredient, Recipe,
                           RecipeIngredient, ShoppingCart, Tag)

from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer
from .utils import generate_report


class TagsViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthorOrReadOnly]

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
        RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values_list(
            'ingredient__name', 'ingredient__measurement_unit', 'amount'
        ).annotate(
            ingredient_amount=Sum('amount')
        )
        return generate_report(
            self, "shopping_list.pdf",
            'Список ингредиентов', "amount", "measurement_unit"
        )
