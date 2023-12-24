from django.views.decorators.csrf import csrf_exempt
import json
from Devices.Serializers.DeviceTypeSerializer import DeviceTypeSerializers
from Authorization.Serializers.UserSerilizers import UserSerializers
from Authorization.Views import result_creator


class DeviceTypeViews:

    @csrf_exempt
    def admin_create_view(self, request):
        if request.method.lower() == "options":
            return result_creator()
        input_data = json.loads(request.body)

        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["Name", "OtherInformation"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, message=f"Please enter {field}")
        name = input_data["Name"]
        other_information = input_data["OtherInformation"]

        result, data = DeviceTypeSerializers.admin_create_serializer(
            token=token, name=name, other_information=other_information)
        if result:
            return result_creator()
        else:
            return result_creator(status="failure", code=403, message=data["message"])

    @csrf_exempt
    def admin_edit_view(self, request):
        if request.method.lower() == "options":
            return result_creator()
        input_data = json.loads(request.body)

        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["Id", "Name", "OtherInformation"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, message=f"Please enter {field}")
        id = input_data["Id"]
        name = input_data["Name"]
        other_information = input_data["OtherInformation"]

        result, data = DeviceTypeSerializers.admin_edit_serializer(
            token=token, id=id, name=name, other_information=other_information)
        if result:
            return result_creator()
        else:
            return result_creator(status="failure", code=403, message=data["message"])

    @csrf_exempt
    def admin_delete_view(self, request):
        if request.method.lower() == "options":
            return result_creator()
        input_data = json.loads(request.body)

        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["Id"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, message=f"Please enter {field}")
        id = input_data["Id"]
        result, data = DeviceTypeSerializers.admin_delete_serializer(
            token=token, id=id)
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
        fields = ["Page", "Count", "Name"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, message=f"Please enter {field}")
        page = input_data["Page"]
        count = input_data["Count"]
        name = input_data["Name"]

        result, data = DeviceTypeSerializers.admin_get_all_serializer(
            token=token, name=name, page=page, count=count)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, message=data["english_message"])

    @csrf_exempt
    def admin_get_one_view(self, request):
        if request.method.lower() == "options":
            return result_creator()
        input_data = json.loads(request.body)
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["Id"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, message=f"Please enter {field}")
        id = input_data['Id']
        result, data = DeviceTypeSerializers.admin_get_one_serializer(
            token=token, id=id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, message=data["english_message"])
