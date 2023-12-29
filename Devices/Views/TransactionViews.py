from django.views.decorators.csrf import csrf_exempt
import json
from Devices.Serializers.TransactionSerializers import TransactionSerializers
from Authorization.Serializers.UserSerilizers import UserSerializers
from Authorization.Views import result_creator


class TransactionViews:

    @csrf_exempt
    def create_view(self, request):
        if request.method.lower() == "options":
            return result_creator()
        input_data = json.loads(request.body)

        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["StripeCode", "Status", "OtherInformation", "Duration"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, message=f"Please enter {field}")
        duration = input_data["Duration"]
        stripe_code = input_data["StripeCode"]
        status = input_data["Status"]
        other_information = input_data["OtherInformation"]
        result, data = TransactionSerializers.create_serializer(
            token=token, stripe_code=stripe_code, status=status, duration=duration,
            other_information=other_information)
        if result:
            return result_creator()
        else:
            return result_creator(status="failure", code=403, message=data["message"])

    @csrf_exempt
    def admin_get_all_views(self, request):
        if request.method.lower() == "options":
            return result_creator()
        input_data = json.loads(request.body)
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["Page", "Count", "Status"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, message=f"Please enter {field}")
        page = input_data["Page"]
        count = input_data["Count"]
        status = input_data["Status"]

        result, data = TransactionSerializers.admin_get_all_serializer(
            token=token, status=status, page=page, count=count)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, message=data["message"])
