from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_classes, name='all_classes'),
    path('add/', views.add_class, name='add_class'),
    path('edit/<int:class_id>/', views.edit_class, name='edit_class'),
    path('delete/<int:class_id>/', views.delete_class, name='delete_class'),
    path('<int:class_id>/', views.class_detail, name='class_detail'),
    path('schedules/', views.class_schedule_list, name='class_schedule_list'),
    path('admin/schedules/', views.admin_schedule_list, name='admin_schedule_list'),
    path('admin/schedules/create/', views.create_schedule, name='create_schedule'),
    path('admin/schedules/bulk-create/', views.bulk_create_schedules, name='bulk_create_schedules'),
]
