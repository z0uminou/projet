from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("home/", views.home, name = "home"),
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('carte/', views.carte_view, name='carte'),
]


