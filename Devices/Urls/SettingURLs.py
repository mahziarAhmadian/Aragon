from django.urls import path
from Devices.Views.SettingViews import SettingViews

setting_views = SettingViews()
urlpatterns = [
    # Super admin urls
    path('admin/create', setting_views.admin_create_view),
    path('admin/getAll', setting_views.admin_get_all_views),

]
