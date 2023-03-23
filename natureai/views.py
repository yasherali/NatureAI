from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from natureai.serializers import UserSerializer, ForgotPasswordSerializer, VerificationSerilizer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class ForgotPasswordAPIView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            new_password = serializer.validated_data.get('new_password')

            User = get_user_model()
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'User not found.'}, status=404)

            user.set_password(new_password)
            user.save()

            return Response({'success': 'Password updated successfully.'}, status=200)
        else:
            return Response(serializer.errors, status=400)


class VerificationAPIView(APIView):
    def post(self, request):
        serializer = VerificationSerilizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=400)

        phone = user.phone
        return Response({'phone': phone})
