import uuid
from datetime import datetime
from django.db import models
from Authorization.models.admins import Admins


# Create your models here.
class CustomDeviceTypeManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def serialize(self, queryset):
        serialized_data = []
        for obj in queryset:
            serialized_obj = {
                "Admin": {
                    "Id": obj.admin.id,
                    "Name": obj.admin.name,
                    "LastName": obj.admin.last_name,
                    "Email": obj.admin.email,
                    "IsSuperAdmin": obj.admin.is_super_admin,
                    "isStaff": obj.admin.is_staff
                },
                "Id": obj.id,
                "Name": obj.name,
                "OtherInformation": obj.other_information,
                "CreateDate": obj.create_date,
            }
            serialized_data.append(serialized_obj)

        return serialized_data


class DeviceTypes(models.Model):
    admin = models.ForeignKey(Admins, on_delete=models.CASCADE, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, null=True)
    other_information = models.JSONField(null=True)
    create_date = models.DateTimeField(
        default=datetime.now, blank=True)
    objects = CustomDeviceTypeManager()

    class Meta:
        db_table = 'DeviceTypes'
