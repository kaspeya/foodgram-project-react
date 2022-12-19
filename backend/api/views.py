from django.contrib.auth import get_user_model
from django.db.models.aggregates import Sum
from django.shortcuts import get_object_or_404
from requests import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from recipe.models import (FavoriteRecipe, Ingredient, Recipe,
                           RecipeIngredient, ShoppingCart, Tag)
from users.models import Follow

from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (FollowSerializer, IngredientSerializer,
                          RecipeSerializer, TagSerializer)
from .utils import generate_report

User = get_user_model()


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
            self, 'shopping_list.pdf',
            'Список ингредиентов', 'amount', 'measurement_unit'
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    @action(
        detail=True,
        permission_classes=(IsAuthenticated,),
        methods=['post', 'delete']
    )
    def follow(self, request, **kwargs):
        user = request.user
        author_id = kwargs.get('id')
        author = get_object_or_404(User, id=author_id)
        following = Follow.objects.filter(
            user=user,
            author=author
        )
        if request.method == 'POST':
            if user == author:
                return Response(
                    {'errors': 'It\'s not allowed to subscribe to yourself.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if following.exists():
                return Response(
                    {'errors': 'You are already subscribed to the user'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = FollowSerializer(
                author,
                context={'request': request},
            )
            Follow.objects.create(
                user=user, author=author
            )
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        if not following.exists():
            return Response(
                {'errors': 'You are not subscribed to the user'},
                status=status.HTTP_400_BAD_REQUEST
            )
        following.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated],
        methods=['get']
    )
    def followings(self, request):
        queryset = User.objects.filter(
            author__user=request.user
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = FollowSerializer(
                page, many=True, context={'request': request}
            )
            return self.get_paginated_response(serializer.data)
        serializer = FollowSerializer(
            queryset, many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    #
    # def following_create(self, serializer):
    #     follow = Follow.objects.create(user=user, author=author)
    #     serializer = FollowSerializer(
    #         follow, context={'request': request}
    #     )
    #     serializer.save(user=self.request.user)
    #
    # @action(detail=True, methods=['get', 'delete'],
    #         permission_classes=[IsAuthenticated])
    # def following(self, request, pk=None):
    #     if request.method == 'GET':
    #         return self.add_obj(Follow, request.user, pk)
    #     if request.method == 'DELETE':
    #         return self.delete_obj(Follow, request.user, pk)
    #     return None
