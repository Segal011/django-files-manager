from django.urls import path
from .views import (
    FileListApiView,
    FileDetailApiView
)

urlpatterns = [
    path('file', FileListApiView.as_view()),
    path('file/<int:todo_id>/', FileDetailApiView.as_view()),
]