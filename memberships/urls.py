from django.urls import path
from . import views

app_name = 'memberships'

urlpatterns = [
    path('', views.membership_plans, name='membership_plans'),
    path('<int:plan_id>/', views.membership_detail, name='membership_detail'),
]
