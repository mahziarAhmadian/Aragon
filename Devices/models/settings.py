import uuid
from datetime import datetime
from django.db import models
from Authorization.models.admins import Admins
from Authorization.models.users import Users
from .device_types import DeviceTypes


# Create your models here.
class CustomSettingManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def serialize(self, queryset):
        serialized_data = []
        for obj in queryset:
            serialized_obj = {
                "Information": obj.information,
            }
            serialized_data.append(serialized_obj)

        return serialized_data


class Settings(models.Model):
    information = models.JSONField(null=True)
    objects = CustomSettingManager()

    class Meta:
        db_table = 'Settings'
