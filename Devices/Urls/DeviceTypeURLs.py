from django.urls import path
from Devices.Views.DeviceTypeViews import DeviceTypeViews

device_type_views = DeviceTypeViews()
urlpatterns = [
    # Super admin urls
    path('admin/create', device_type_views.admin_create_view),
    path('admin/edit', device_type_views.admin_edit_view),
    path('admin/delete', device_type_views.admin_delete_view),
    path('admin/getAll', device_type_views.admin_get_all_views),
    path('admin/getOne', device_type_views.admin_get_one_view),

]
