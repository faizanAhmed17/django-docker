from django.urls import path
from .views import ListCreateSongsView, LoginView


urlpatterns = [
    path('songs/', ListCreateSongsView.as_view(), name="songs-list-create"),
    path('auth/login/', LoginView.as_view(), name="auth-login")
]