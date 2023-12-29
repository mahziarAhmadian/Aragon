from django.urls import path
from Devices.Views.DeviceViews import DeviceViews

device_views = DeviceViews()
urlpatterns = [
    path('create', device_views.admin_create_view),
    path('admin/getAll', device_views.admin_get_all_views)

]
