from django.views.decorators.csrf import csrf_exempt
import json
from Devices.Serializers.DeviceSerializers import DeviceSerializers
from Authorization.Serializers.UserSerilizers import UserSerializers
from Authorization.Views import result_creator


class DeviceViews:

    @csrf_exempt
    def admin_create_view(self, request):
        if request.method.lower() == "options":
            return result_creator()
        input_data = json.loads(request.body)

        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["Name", "Serial", "TypeId","OtherInformation"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, message=f"Please enter {field}")
        name = input_data["Name"]
        serial = input_data["Serial"]
        type_id = input_data["TypeId"]
        other_information = input_data["OtherInformation"]

        result, data = DeviceSerializers.admin_create_serializer(
            token=token, name=name, serial=serial, type_id=type_id,other_information=other_information)
        if result:
            return result_creator()
        else:
            return result_creator(status="failure", code=403, message=data["message"])

    @csrf_exempt
    def user_get_all_views(self, request):
        if request.method.lower() == "options":
            return result_creator()
        input_data = json.loads(request.body)

        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["Page", "Count", "Serial"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, message=f"Please enter {field}")
        page = input_data["Page"]
        count = input_data["Count"]
        serial = input_data["Serial"]

        result, data = DeviceSerializers.user_get_all_serializer(page=page, count=count,
                                                                 token=token, serial=serial)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, message=data["message"])

    @csrf_exempt
    def staff_admin_assign_user_views(self, request):
        if request.method.lower() == "options":
            return result_creator()
        input_data = json.loads(request.body)
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["UserId", "Serial"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, message=f"Please enter {field}")
        serial = input_data["Serial"]
        user_id = input_data["UserId"]

        result, data = DeviceSerializers.staff_admin_assign_user_serializer(
            token=token, serial=serial, user_id=user_id)
        if result:
            return result_creator(data=data)
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

        result, data = DeviceSerializers.admin_get_all_serializer(
            token=token, name=name, page=page, count=count)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, message=data["english_message"])

    @csrf_exempt
    def user_get_one_view(self, request):
        if request.method.lower() == "options":
            return result_creator()
        input_data = json.loads(request.body)
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["Serial"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, message=f"Please enter {field}")
        serial = input_data["Serial"]
        result, data = DeviceSerializers.user_get_one_serializer(token=token, serial=serial)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, message=data["message"])

    @csrf_exempt
    def admin_get_one_view(self, request):
        if request.method.lower() == "options":
            return result_creator()
        input_data = json.loads(request.body)
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["Serial"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, message=f"Please enter {field}")
        serial = input_data["Serial"]
        result, data = DeviceSerializers.admin_get_one_serializer(token=token, serial=serial)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, message=data["english_message"])

    @csrf_exempt
    def user_send_order_view(self, request):
        if request.method.lower() == "options":
            return result_creator()
        input_data = json.loads(request.body)
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["Serial"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, message=f"Please enter {field}")
        serial = input_data["Serial"]
        result, data = DeviceSerializers.user_send_order_serializer(token=token, serial=serial)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, message=data["message"])

    @csrf_exempt
    def user_devices_view(self, request):
        if request.method.lower() == "options":
            return result_creator()
        input_data = json.loads(request.body)
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["UserIDList"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, message=f"Please enter {field}")
        user_id_list = input_data["UserIDList"]

        result, data = DeviceSerializers.user_devices_serializer(
            token=token, user_id_list=user_id_list)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, message=data["english_message"])