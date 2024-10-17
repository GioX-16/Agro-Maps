from django.urls import path
from . import views

urlpatterns = [
    path('fertilidad/', views.mapa_fertilidad_view, name='mapa_fertilidad'), 
    path('panel/', views.dashboard_view, name='dashboard'),
    path('mapa/', views.mapa_fertilidad_view, name='mapa'),
    path('study/', views.study_view, name='study'),
    path('formstudy/', views.form_study_view, name='formstudy'),
    path('register-soil-study/', views.register_soil_study, name='register_soil_study'),

]