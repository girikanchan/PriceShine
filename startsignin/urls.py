
from django.conf import settings
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/',views.SignupPage,name ='signup'),
    path('login/',views.LoginPage,name='login'),
    path('home/',views.HomePage,name='home'),
    path('logout/',views.LogoutPage,name='logout'),
    path('clothes/',views.Clothes,name='Clothes'),
    path('grossary/',views.Grossary,name='Grossary'),
    path('',views.About,name='About'),
    path('medicine/',views.Medicine,name='medicine'),
    path('grocery/',views.Grocery,name='grocery'),
]
