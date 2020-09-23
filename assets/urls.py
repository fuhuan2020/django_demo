from django.urls import path
from assets import views


app_name = 'assets'


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('kvm/', views.kvm, name='kvm'),
    path('index/', views.index, name='index'),
    path('', views.dashboard),
]