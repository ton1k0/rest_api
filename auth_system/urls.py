from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.user_registration, name='user-registration'),
    path('login/', views.user_login, name='user-login'),
    path('refresh/', views.token_refresh, name='token-refresh'),
    path('logout/', views.user_logout, name='user-logout'),
    path('me/', views.user_info, name='user-info'),
    path('me/update/', views.update_user_info, name='update-user-info'),
]