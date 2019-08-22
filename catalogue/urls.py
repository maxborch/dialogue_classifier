from django.urls import path

from .views import (

    upload_file,
    upload_detail,
    my_uploads,
    edit_upload,
    delete_archive,
    UploadDeleteView,
    download_file
)

urlpatterns = [

    path('case/add/', upload_file, name='file-upload'),
    path('upload/<int:upload_id>/', upload_detail, name='upload-detail'),
    path('upload/<int:pk>/delete/', UploadDeleteView.as_view(), name='upload-delete'),
    path('upload/<int:upload_id>/edit/', edit_upload, name='upload-edit'),
    path('my-uploads/', my_uploads, name='my-uploads'),
    path('archive/<int:archive_id>/delete', delete_archive, name='delete-archive'),
    path('download/<int:upload_id>/', download_file, name='download_file')

]
