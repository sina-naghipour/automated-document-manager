from django.urls import path
from docs.views import (
    Upload, DocumentListView, download_file,
    delete_document, Trash, restore_document,
    permenant_delete, empty_trash
)

from django.conf import settings
from django.conf.urls.static import static


app_name = 'docs'

urlpatterns = [
    path('upload/', Upload.as_view(), name='upload'),
    path('list/', DocumentListView.as_view(), name='list'),
    path('download/<path:path>/', download_file, name='download'),
    path('delete/<int:pk>/', delete_document, name='delete'),
    path('restore/<int:pk>/', restore_document, name='restore'),
    path('permenant-delete/<int:pk>/', permenant_delete, name='permanent_delete'),
        path('empty-trash/', empty_trash, name='empty_trash'),
    path('trash/', Trash.as_view(), name='trash'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)