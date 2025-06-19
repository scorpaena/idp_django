from django.urls import path, include
from game.views import GameSessionViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'sessions', GameSessionViewSet, basename='gamesession')

urlpatterns = [
    path('', include(router.urls)),
]
