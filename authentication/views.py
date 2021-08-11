from authentication.mail import sendMail
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from . import serializer
from rest_framework.decorators import authentication_classes
from .token import StaticTokenAuthentication
from django.core.validators import validate_email


@api_view(["POST"])
@authentication_classes([StaticTokenAuthentication])
def RegisterView(request):
    resp = {
        "success": False,
        "errors": {},
        "tokens": {}
    }
    ser = serializer.RegisterSerializer(data=request.data)
    if ser.is_valid():
        user, otp = ser.save()
        resp["success"] = True
        resp["tokens"] = user.token()
        resp["otp"] = otp
        return Response(resp, status=status.HTTP_201_CREATED)
    else:
        resp["errors"] = ser.errors
        return Response(resp, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([StaticTokenAuthentication])
def GoogleRegisterView(request):
    resp = {
        "success": False,
        "errors": {},
        "tokens": {}
    }
    ser = serializer.GoogleRegisterSerializer(data=request.data)
    if ser.is_valid():
        user = ser.validated_data.get("auth_token", {})
        resp["tokens"] = {} if user == {} else user.token()
        resp["success"] = True
        return Response(resp, status=status.HTTP_201_CREATED)
    else:
        resp["errors"] = ser.errors
        return Response(resp, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([StaticTokenAuthentication])
def LoginView(request):
    data = {
        "success": False,
        "is_verified": False,
        "tokens": {},
        "errors": {}
    }
    ser = serializer.LoginSerializer(data=request.data)
    if ser.is_valid():
        user = ser.validated_data.get("email")
        data["success"] = True
        data["is_verified"] = user.is_verified
        data["tokens"] = user.token()
        if not user.is_verified:
            data["otp"] = sendMail(user.email)
        return Response(data, status=status.HTTP_200_OK)
    else:
        data["errors"] = ser.errors
        data["errors"]["description"] = "Invaild Email / Password. Try again"
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([StaticTokenAuthentication])
def GoogleLoginView(request):
    data = {
        "success": False,
        "tokens": {},
        "errors": {}
    }
    ser = serializer.GoogleLoginSerializer(data=request.data)
    if ser.is_valid():
        user = ser.validated_data.get("auth_token")
        data["success"] = True
        if not user.is_verified:
            user.is_verified= True
            user.save()
        data["tokens"] = user.token()
        return Response(data, status=status.HTTP_200_OK)
    else:
        data["errors"] = ser.errors
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@authentication_classes([StaticTokenAuthentication])
def ResendOTP(request):
    data = {
        "success": False,
        "otp":0,
        "errors":{}
    }
    email = request.data.get("email", None)
    if email!=None:
        try:
            validate_email(email)
            data["otp"]=sendMail(email)
            data["success"]=True
        except Exception as e:
            data["errors"]={"email":list(e)}
    else:
        data["errors"]={"email":["This field is required."]}

    return Response(data, status=status.HTTP_400_BAD_REQUEST)
