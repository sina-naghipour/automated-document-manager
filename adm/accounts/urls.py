from django.urls import path
from accounts.views import (
    Register, Login, Dashboard, ProfileView,
    Logout, CreateUserView, EditUserView, DetailUserView,
    DeleteUserView
)
app_name = 'accounts'

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('logout/', Logout.as_view(), name='logout'),
    path('users/create/', CreateUserView.as_view(), name='create_user'),
    path('users/edit/', EditUserView.as_view(), name='edit_user'),
    path('users/delete/<int:id>/', DeleteUserView.as_view(), name='delete_user'),
    path('users/detail/<int:id>/ ', DetailUserView.as_view(), name='detail_user'),
    path('users/profile/', ProfileView.as_view(), name='profile'),
]
