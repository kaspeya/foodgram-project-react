from api.views import (FollowViewSet, IngredientsViewSet, RecipeViewSet,
                       TagsViewSet, UserViewSet, get_token, sign_up)
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

app_name = 'api'

router = routers.DefaultRouter()
router.register('tags', TagsViewSet)
router.register('ingredients', IngredientsViewSet)
router.register('recipes', RecipeViewSet)
router.register('users', UserViewSet)
router.register('follow', FollowViewSet, basename='follow')


urlpatterns = [
    path('', include(router.urls)),

]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', sign_up, name='signup'),
    path('v1/auth/token/', get_token, name='gettoken'),
    path('v1/jwt/create/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/jwt/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('v1/jwt/verify/', TokenVerifyView.as_view(),
         name='token_verify')
]
