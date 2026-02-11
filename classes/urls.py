from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_classes, name='all_classes'),
    path('<int:class_id>/', views.class_detail, name='class_detail'),
    path('schedules/', views.class_schedule_list, name='class_schedule_list'),
    path('admin/schedules/', views.admin_schedule_list, name='admin_schedule_list'),
    path('admin/schedules/create/', views.create_schedule, name='create_schedule'),
    path('admin/schedules/bulk-create/', views.bulk_create_schedules, name='bulk_create_schedules'),
]
