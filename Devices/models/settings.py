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
                "Id": obj.id,
                "Information": obj.information
            }
            serialized_data.append(serialized_obj)

        return serialized_data


class Settings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    information = models.JSONField(null=True)
    bool = models.BooleanField(default=True)
    objects = CustomSettingManager()

    class Meta:
        db_table = 'Settings'
