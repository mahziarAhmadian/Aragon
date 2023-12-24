import uuid
from datetime import datetime
from django.db import models
from Authorization.models.admins import Admins
from Authorization.models.users import Users


# Create your models here.
class CustomDeviceManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def serialize(self, queryset):
        serialized_data = []
        for obj in queryset:
            serialized_obj = {
                "Serial": obj.serial,
                "Admin": obj.admin,
                "User": obj.user,
                "Name": obj.name,
                "OtherInformation": obj.other_information,
                "CreateDate": obj.create_date,
            }
            if obj.admin is not None:
                serialized_obj['Admin'] = {
                    "Id": obj.admin.id,
                    "Name": obj.admin.name,
                    "LastName": obj.admin.last_name,
                    "Email": obj.admin.email,
                    "IsSuperAdmin": obj.admin.is_super_admin,
                    "isStaff": obj.admin.is_staff
                }
            if obj.user is not None:
                serialized_obj['User'] = {
                    "Id": obj.user.id,
                    "Name": obj.user.name,
                    "LastName": obj.user.last_name,
                    "Email": obj.user.email,
                }
            serialized_data.append(serialized_obj)

        return serialized_data


class Devices(models.Model):
    admin = models.ForeignKey(Admins, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    serial = models.CharField(max_length=200, primary_key=True, unique=True)
    name = models.CharField(max_length=200, null=True)
    other_information = models.JSONField(null=True)
    create_date = models.DateTimeField(
        default=datetime.now, blank=True)
    objects = CustomDeviceManager()

    class Meta:
        db_table = 'Devices'
