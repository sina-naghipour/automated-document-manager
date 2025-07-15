from django.urls import path
from accounts.views import Register, Login, Dashboard, Logout

app_name = 'accounts'

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('logout/', Logout.as_view(), name='logout'),
]
