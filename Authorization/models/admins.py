import uuid
from django.contrib.postgres.fields import ArrayField
from django.db import models
from datetime import datetime


class CustomAdminManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def serialize(self, queryset):
        serialized_data = []
        for obj in queryset:
            serialized_obj = {
                "Id": obj.id,
                "Email": obj.email,
                "Name": obj.name,
                "LastName": obj.last_name,
                "IsSuperAdmin": obj.is_super_admin,
                "isStaff": obj.is_staff,
                "Permissions": obj.permissions,
                "OtherInformation": obj.other_information,
                "CreateDate": obj.create_date,
                "Images": obj.admin_images
            }
            serialized_data.append(serialized_obj)
        return serialized_data


class Admins(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, unique=True)
    is_super_admin = models.BooleanField()
    is_staff = models.BooleanField()
    password = models.CharField(max_length=200)
    permissions = ArrayField(models.CharField(max_length=100))
    other_information = models.JSONField()
    create_date = models.DateTimeField(
        default=datetime.now, blank=True)
    admin_images = ArrayField(models.CharField(max_length=400), default=list, null=True)

    objects = CustomAdminManager()

    class Meta:
        db_table = 'Admins'
