# credit_bank/urls.py
from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('apply/', views.apply_credit, name='apply_credit'),
    path('register/', views.register, name='register'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('accounts/', include('django.contrib.auth.urls')),
]