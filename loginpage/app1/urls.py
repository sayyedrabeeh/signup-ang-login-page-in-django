
from django.urls import path,include
from .views import authview,home
from . import views

urlpatterns = [
    path ('home/',home,name='home'),
    path('',authview,name='authview'),
    # path("accounts/", include("django.contrib.auth.urls")),
    path('logout/', views.custom_logout, name='logout'),
    path('login/', views.login_view, name='login'),
    

]
