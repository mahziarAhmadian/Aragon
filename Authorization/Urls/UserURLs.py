from django.urls import path
from Authorization.Views.UserViews import UserViews

user_views = UserViews()
urlpatterns = [
    path('admin/staff/create', user_views.staff_admin_create_user_view),

    path('user/login', user_views.user_login_view),
    path('user/getProfile', user_views.user_get_profile_view),
    path('user/edit', user_views.user_edit_view),
    path('user/webhook', user_views.user_web_hook_view),
    # path('user/getDevices', admins_view.admin_edit_view),
    # # path('user/byTime', admins_view.admin_edit_view),

    path('admin/delete', user_views.admin_delete_view),
    path('admin/getOne', user_views.admin_get_one_view),
    path('admin/getAll', user_views.admin_get_all_views),
]
