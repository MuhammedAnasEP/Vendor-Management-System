from rest_framework import serializers
from .models import Vendor, PurchaseOrder
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class TokenObtainPairSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        # Your authentication logic here to validate user credentials
        user = authenticate(username=username, password=password)

        if user:
            data['user'] = user

        return data


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

class VendorPerformanceSerializer(serializers.Serializer):
    on_time_delivery_rate = serializers.FloatField()
    quality_rating_avg = serializers.FloatField()
    average_response_time = serializers.FloatField()
    fulfillment_rate = serializers.FloatField()