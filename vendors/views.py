from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Vendor, PurchaseOrder
from django.utils import timezone
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    VendorSerializer,
    PurchaseOrderSerializer,
    VendorPerformanceSerializer,
    UserRegistrationSerializer,
    UserLoginSerializer,
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
    )


# Create your views here.

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]



class UserLoginView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user', None)
        
        if user:
            refresh = RefreshToken.for_user(user)
            token = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(token, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User not found in validated data."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class VendorListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated | AllowAny]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated | AllowAny]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated | AllowAny]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated | AllowAny]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class VendorPerformanceView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated | AllowAny]
    queryset = Vendor.objects.all()
    serializer_class = VendorPerformanceSerializer
    lookup_url_kwarg = 'vendor_id'

    def retrieve(self, request, *args, **kwargs):
        vendor = self.get_object()
        serializer = self.get_serializer(vendor)
        return Response(serializer.data)

class AcknowledgePurchaseOrderView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated | AllowAny]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_url_kwarg = 'po_id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.acknowledgment_date = timezone.now()
        instance.save()

        # Trigger the recalculation of average_response_time
        vendor = instance.vendor
        vendor.average_response_time = vendor.calculate_average_response_time()
        vendor.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
