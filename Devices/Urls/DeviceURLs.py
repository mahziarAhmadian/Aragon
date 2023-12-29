from django.urls import path
from Devices.Views.DeviceViews import DeviceViews

device_views = DeviceViews()
urlpatterns = [
    # Super admin urls
    path('admin/create', device_views.admin_create_view),
    # Super admin and Staff urls
    path('admin/getAll', device_views.admin_get_all_views),
    path('admin/getOne', device_views.admin_get_one_view),

    # Staff admin urls
    path('admin/staff/assignUser', device_views.staff_admin_assign_user_views),
    # User urls
    path('user/getAll', device_views.user_get_all_views),
    path('user/getOne', device_views.user_get_one_view),
    path('user/sendOrder', device_views.user_send_order_view),
    path('user/devices', device_views.user_devices_view),

]
