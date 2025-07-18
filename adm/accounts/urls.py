from django.urls import path
from accounts.views import (
    Register, Login, Dashboard, 
    Logout, CreateUserView, EditUserView,
    RoleManagement, AccessManagementView
)
app_name = 'accounts'

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('logout/', Logout.as_view(), name='logout'),
    path('users/create/', CreateUserView.as_view(), name='create_user'),
    path('users/edit/', EditUserView.as_view(), name='edit_user'),
    path('users/roles/', RoleManagement.as_view(), name='access_management'),
    path('users/access/', AccessManagementView.as_view(), name='role_management'),
]
