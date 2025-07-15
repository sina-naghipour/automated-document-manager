from django.urls import path
from docs.views import Upload
app_name = 'docs'

urlpatterns = [
    path('upload/', Upload.as_view(), name='upload'),
]