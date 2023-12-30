import uuid
from datetime import datetime
from django.db import models
from Authorization.models.users import Users


# Create your models here.
class CustomTransactionsManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def serialize(self, queryset):
        serialized_data = []
        for obj in queryset:
            serialized_obj = {
                "Id": obj.id,
                "CompletedTime": obj.completed_time,
                "StripeCode": obj.stripe_code,
                "Status": obj.status,
                "OtherInformation": obj.other_information,
                "CreateTime": obj.create_time,
                "Duration": obj.duration,
                "Price": obj.price,
                "Count": obj.count,
                "User": {
                    "Id": obj.user.id,
                    "Name": obj.user.name,
                    "LastName": obj.type.last_name,
                    "Email": obj.type.email,
                }
            }
            serialized_data.append(serialized_obj)

        return serialized_data


class Transactions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    duration = models.CharField(max_length=30)
    stripe_code = models.CharField(max_length=500)
    completed_time = models.DateTimeField(null=True)
    status = models.IntegerField()
    price  = models.IntegerField(null=True)
    count  = models.IntegerField(null=True)
    other_information = models.JSONField(null=True)
    create_time = models.DateTimeField(
        default=datetime.now, blank=True)
    objects = CustomTransactionsManager()

    class Meta:
        db_table = 'Transactions'

