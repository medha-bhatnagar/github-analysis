from django.urls import path
from . import views

urlpatterns = [
    path('analyze/<str:username>/', views.analyze_profile, name='analyze_profile'),
]