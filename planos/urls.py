from django.urls import path
from . import views

urlpatterns = [
    path('', views.planos, name='planos'),
]