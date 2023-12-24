from django.urls import path
from Authorization.Views.AdminViews import AdminViews


admins_view = AdminViews()
urlpatterns = [
    path('admin/login', admins_view.admin_login_view),
    path('admin/create', admins_view.admin_add_view),
    path('admin/edit', admins_view.admin_edit_view),
    path('admin/delete', admins_view.admin_delete_view),
    path('admin/getOne', admins_view.admin_get_one_view),
    path('admin/getAll', admins_view.admin_get_all_views),
]
