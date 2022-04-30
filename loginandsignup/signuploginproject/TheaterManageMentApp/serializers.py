import math
import random

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import *


class AdminRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminRegisterModel
        fields = ['AdminId', 'Email', 'Password', 'MobileNumber', 'CreatedDate', 'UpdatedDate', 'Status']


def generateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP


class Templateserializers(serializers.ModelSerializer):
    class Meta:
        model = AdminRegisterModel
        fields = ['AdminId', 'otp']

    def create(self, validated_data):
        user = AdminRegisterModel.objects.create(AdminId=validated_data['AdminId'], otp=generateOTP())

        user.save()
        # print(user.otp)
        return user


class AdminLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminRegisterModel
        fields = ['id', 'Email', 'MobileNumber', 'Password']
        extra_kwargs = {'Password': {'write_only': True}}

    def create(self, validated_data):
        user = AdminRegisterModel.objects.get(Email=validated_data['Email'])
        user.save()
        return user


class MoviesPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieListModel
        fields = "__all__"
