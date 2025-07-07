from django.urls import path, include
from game.views import GameSessionViewSet, GameResultViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'sessions', GameSessionViewSet, basename='gamesession')
router.register(r'results', GameResultViewSet, basename='gameresult')

urlpatterns = [
    path('', include(router.urls)),
]
