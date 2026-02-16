from django.urls import path
from . import views

app_name = 'memberships'

urlpatterns = [
    path('', views.membership_plans, name='membership_plans'),
    path('<int:plan_id>/', views.membership_detail, name='membership_detail'),
    path('purchase/<int:plan_id>/', views.purchase_membership, name='purchase_membership'),
    path('create-subscription/', views.create_subscription, name='create_subscription'),
    path('activate/<int:plan_id>/', views.activate_membership, name='activate_membership'),
    path('confirmation/<int:membership_id>/', views.membership_confirmation, name='membership_confirmation'),
]
