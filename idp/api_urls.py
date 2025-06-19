from django.urls import path, include

urlpatterns = [
    path('user_account/', include('user_account.urls')),
    path("game/", include("game.urls")),
]
