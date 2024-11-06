from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("home/", views.home, name = "home"),
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='carte'),
    path('rucher/<str:rucher_id>/', views.vue_rucher, name='vue_rucher'),
]


