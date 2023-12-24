from django.views.decorators.csrf import csrf_exempt
import json
from Authorization.Serializers.AdminSerilizer import AdminSerializers
from Authorization.Views import result_creator


class AdminViews:

    @csrf_exempt
    def admin_login_view(self, request):

        if request.method.lower() == "options":
            return result_creator()
        input_data = json.loads(request.body)
        fields = ["Email", "Password"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, message=f"Please enter {field}")
        email = input_data["Email"]
        password = input_data["Password"]
        result, data = AdminSerializers.admin_login_serializer(email=email, password=password)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, message="email or password is incorrect")

    @csrf_exempt
    def admin_add_view(self, request):
        if request.method.lower() == "options":
            return result_creator()
        input_data = json.loads(request.body)

        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["Name", "LastName", "Email", "isStaff", "Password", "OtherInformation"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, message=f"Please enter {field}")
        name = input_data["Name"]
        last_name = input_data["LastName"]
        email = input_data["Email"]
        is_staff = input_data["isStaff"]
        password = input_data["Password"]
        other_information = input_data["OtherInformation"]
        result, data = AdminSerializers.admin_add_serializer(
            token=token, name=name, last_name=last_name, email=email,
            is_staff=is_staff, password=password,
            other_information=other_information)
        if result:
            return result_creator(data=data)
        else:
            print(f"in else : {data}")
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
        fields = ["Id", "Name", "LastName", "Email", "isStaff", "Password", "OtherInformation"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, message=f"Please enter {field}")
        id = input_data["Id"]
        name = input_data["Name"]
        last_name = input_data["LastName"]
        email = input_data["Email"]
        is_staff = input_data["isStaff"]
        password = input_data["Password"]
        other_information = input_data["OtherInformation"]
        result, data = AdminSerializers.admin_edit_serializer(
            token=token, id=id, name=name, last_name=last_name, email=email, is_staff=is_staff, password=password,
            other_information=other_information)
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
        result, data = AdminSerializers.admin_delete_serializer(token, id=id)
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
        fields = ["Id"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, message=f"Please enter {field}")
        id = input_data["Id"]
        result, data = AdminSerializers.admin_get_one_serializer(token=token, id=id)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, message=data["english_message"])

    @csrf_exempt
    def admin_get_all_views(self, request):
        if request.method.lower() == "options":
            return result_creator()
        input_data = json.loads(request.body)
        if "Token" in request.headers:
            token = request.headers["Token"]
        else:
            token = ''
        fields = ["Page", "Count", "Name", "IsSuperAdmin", "isStaff"]
        for field in fields:
            if field not in input_data:
                return result_creator(status="failure", code=406, message=f"Please enter {field}")
        page = input_data["Page"]
        count = input_data["Count"]
        name = input_data["Name"]
        is_super_admin = input_data["IsSuperAdmin"]
        is_staff = input_data["isStaff"]
        result, data = AdminSerializers.admin_get_all_serializer(
            token=token, name=name, page=page, count=count, is_super_admin=is_super_admin, is_staff=is_staff)
        if result:
            return result_creator(data=data)
        else:
            return result_creator(status="failure", code=403, message=data["english_message"])
