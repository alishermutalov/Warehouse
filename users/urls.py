from django.urls import path
from .views import CreateUserAPIView, DashboardAPIView, UpdateUserInfoAPIView, \
    ChangePasswordAPIView, LoginAPIView, LoginRefreshAPIView, LogoutAPIView

urlpatterns = [
    path('register/', CreateUserAPIView.as_view(), name='register'),
    path('update/', UpdateUserInfoAPIView.as_view(), name='update'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='change-password'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('login-refresh/', LoginRefreshAPIView.as_view(), name='login-refresh'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('dashboard/', DashboardAPIView.as_view(), name='dashboard'),
]
