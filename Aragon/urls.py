"""Aragon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from Authorization.Urls import AdminURLs, UserURLs
from Devices.Urls import DeviceURLs
from Devices.Urls import DeviceTypeURLs
from Devices.Urls import TransactionURLs
from Devices.Urls import SettingURLs

urlpatterns = [
    path('admins/', include(AdminURLs)),
    path('users/', include(UserURLs)),
    path('devices/', include(DeviceURLs)),
    path('types/', include(DeviceTypeURLs)),
    path('transactions/', include(TransactionURLs)),
    path('settings/', include(SettingURLs)),
]
