from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('add_user/', views.add_user, name="adduser"),
    path('user/', views.user_list, name='user_list'),  # Lists all users or filtered by shift
    path('user/<int:user_id>/', views.user_detail, name='user_detail'),
    path('delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('user/<int:user_id>/add_amount/', views.add_daily_amount, name='add_daily_amount'),
    path('user/<int:user_id>/summary/', views.user_summary, name='user_summary'),
    path('update-status/<int:record_id>/', views.update_status, name='update_status'),
    path('all-orders/', views.all_orders_view, name='all_orders'),
]
