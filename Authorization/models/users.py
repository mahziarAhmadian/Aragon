import uuid
from datetime import datetime
from django.contrib.postgres.fields import ArrayField
from django.db import models
from .admins import Admins

# Create your models here.
class CustomUserManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def serialize(self, queryset):
        serialized_data = []
        for obj in queryset:
            serialized_obj = {
                "admin": {
                    "Id": obj.admin.id,
                    "Name": obj.admin.name,
                    "LastName": obj.admin.last_name,
                    "Email": obj.admin.email,
                    "IsSuperAdmin": obj.admin.is_super_admin,
                    "isStaff": obj.admin.is_staff
                },
                "Id": obj.id,
                "Email": obj.email,
                "Name": obj.name,
                "LastName": obj.last_name,
                "Password": obj.password,
                "OtherInformation": obj.other_information,
                "CreateDate": obj.create_date,
                "Images": obj.images,
            }
            serialized_data.append(serialized_obj)

        return serialized_data


class Users(models.Model):
    admin = models.ForeignKey(Admins, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=200, null=True)
    other_information = models.JSONField(null=True)
    create_date = models.DateTimeField(
        default=datetime.now, blank=True)
    images = ArrayField(models.CharField(max_length=400), default=list, null=True)
    objects = CustomUserManager()

    class Meta:
        db_table = 'Users'
