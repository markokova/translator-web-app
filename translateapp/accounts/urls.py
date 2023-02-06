from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
        path('dashboard', views.dashboard, name="dashboard"),
        path('profile/<int:user_id>', views.profile, name="profile"),
        path('register', views.register, name="register"),
]
