from django.urls import path
from django.contrib.auth import views as auth_views
from .views import signup, profile, order_history

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', signup, name='signup'),
    path('profile/', profile, name='profile'),
    path('orders/', order_history, name='order_history'),
]