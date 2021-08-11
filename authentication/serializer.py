from rest_framework import serializers
from .models import BasicDetails, User
from .google import Google
from django.db import transaction
from .mail import sendMail


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=5, max_length=15, write_only=True)

    class Meta:
        model = User
        fields = ["email", "password"]
        extra_kwargs = {
            'email': {'validators': []},
        }

    def validate(self, attrs):
        email = attrs.get("email", "")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"errors": "%s is already register with us" % email})
        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        otp = sendMail(user.email)
        return user, otp


class GoogleRegisterSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = Google.validate(auth_token)

        if User.objects.filter(email=user_data["email"]).exists():
            raise serializers.ValidationError(
                "%s is already register with us" % user_data['email'])
        try:
            with transaction.atomic():
                user = User.objects.create_user(email=user_data["email"])
                user.is_verified = True
                first_name = user_data["given_name"]
                last_name = user_data["family_name"]
                BasicDetails.objects.create(
                    first_name=first_name, last_name=last_name, user=user)
                user.provider = "Google"
                user.save()
                return user
        except:
            raise serializers.ValidationError(
                "Something went Wrong. Try again!")


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        max_length=255, write_only=True)

    def validate_email(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("E-mail doesn't exists")

    def validate(self, attrs):
        email = attrs.get("email")
        if isinstance(email, User):
            if not email.check_password(attrs.get("password", "")):
                raise serializers.ValidationError(
                    {"password": "Password mismatch"})
        else:
            raise serializers.ValidationError(
                {"email": "User instance not found"})
        return super().validate(attrs)


class GoogleLoginSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = Google.validate(auth_token)
        try:
            return User.objects.get(email=user_data["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "%s is not register with us. Kindly share the verified email." % user_data['email'])