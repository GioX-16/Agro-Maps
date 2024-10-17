from django.urls import path
from . import views
from .views import login_view
from django.urls import path, include


urlpatterns = [
    path('', login_view, name='login'),
    path('register/', views.register, name='register'),
]
