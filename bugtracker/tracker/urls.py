from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = ([
    path('', views.task_list, name='task_list'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('attachments/<str:filename>/', views.download_file, name='download_file'),
])

