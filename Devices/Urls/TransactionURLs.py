from django.urls import path
from Devices.Views.TransactionViews import TransactionViews

transaction_views = TransactionViews()
urlpatterns = [
    path('user/create', transaction_views.user_create_view),
    path('admin/getAll', transaction_views.admin_get_all_views),
    path('user/getAll', transaction_views.user_get_all_views),

]
