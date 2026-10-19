from django.urls import path
from . import views

urlpatterns = [
    path('dashboard',views.dashboard,name='dashboard'),
    path('rules',views.rules,name='rules'),
    path('client-rules',views.client_rules,name='client_rules'),


]