from django.urls import path
from . import views

urlpatterns = [
     path('', views.mapa_fertilidad_view, name='mapa_fertilidad'),
]