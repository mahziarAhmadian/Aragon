from django.views.decorators.csrf import csrf_exempt
import json
from Authorization.Serializers.UserSerilizers import UserSerializers
from Authorization.Views import result_creator


class UserViews:

    @csrf_exempt
    def user_login_view(self, request):

        if request.method.lower() == "options":
            return result_creator()
        input_data = json.loads(request.body)
        fields = ["Email", "Password"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, message=f"Please enter {field}")
        email = input_data["Email"]
        password = input_data["Password"]
        result, data = UserSerializers.user_login_serializer(email=email, password=password)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, message="email or password is incorrect")

    @csrf_exempt
    def user_edit_view(self, request):
        if request.method.lower() == "options":
            return result_creator()
        input_data = json.loads(request.body)

        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = [ "Name", "LastName", "Email", "Password", "OtherInformation"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, message=f"Please enter {field}")
        name = input_data["Name"]
        last_name = input_data["LastName"]
        email = input_data["Email"]
        password = input_data["Password"]
        other_information = input_data["OtherInformation"]
        result, data = UserSerializers.admin_edit_serializer(
            token=token,  name=name, last_name=last_name, email=email,  password=password,
            other_information=other_information)
        if result:
            return result_creator()
        else:
            return result_creator(status="failure", code=403, message=data["message"])

    @csrf_exempt
    def staff_admin_create_user_view(self, request):
        if request.method.lower() == "options":
            return result_creator()
        input_data = json.loads(request.body)

        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["Name", "LastName", "Email", "Password", "OtherInformation"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, message=f"Please enter {field}")
        name = input_data["Name"]
        last_name = input_data["LastName"]
        email = input_data["Email"]
        password = input_data["Password"]
        other_information = input_data["OtherInformation"]
        result, data = UserSerializers.staff_admin_create_user_serializer(
            token=token, name=name, last_name=last_name, email=email, password=password,
            other_information=other_information)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, message=data["message"])

    @csrf_exempt
    def user_get_profile_view(self, request):
        if request.method.lower() == "options":
            return result_creator()
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''

        result, data = UserSerializers.user_get_profile_serializer(token=token)
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

        result, data = UserSerializers.admin_get_all_serializer(
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
        id = input_data["Id"]
        result, data = UserSerializers.admin_get_one_serializer(token=token, id=id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, message=data["english_message"])

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
        result, data = UserSerializers.admin_delete_serializer(token, id=id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, message=data["message"])
