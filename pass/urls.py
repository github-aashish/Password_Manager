from django.urls import path
from . import views

urlpatterns = [
    path('',views.login),
    path('signup',views.signup),
    path('home',views.home),
    path('add-pass',views.add_pass),
    path('logout',views.logout),
    path('check-password/<int:web_id>',views.check_password),
]