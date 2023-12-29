from django.views.decorators.csrf import csrf_exempt
import json
from Devices.Serializers.SettingSerializer import SettingSerializers
from Authorization.Serializers.UserSerilizers import UserSerializers
from Authorization.Views import result_creator


class SettingViews:

    @csrf_exempt
    def admin_create_view(self, request):
        if request.method.lower() == "options":
            return result_creator()
        input_data = json.loads(request.body)

        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["Information"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, message=f"Please enter {field}")
        information = input_data["Information"]

        result, data = SettingSerializers.admin_create_serializer(
            token=token, information=information)
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
        fields = ["Page", "Count"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, message=f"Please enter {field}")
        page = input_data["Page"]
        count = input_data["Count"]

        result, data = SettingSerializers.admin_get_all_serializer(
            token=token, page=page, count=count)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, message=data["message"])
