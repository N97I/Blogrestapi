from users.serializers import UserCreateSerializer, UserAuthSerializer, UserConfirmSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from users.models import ConfirmationCode
from rest_framework.views import APIView



class AuthAPIView(APIView):
    def post(self, request):
        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})    
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    

class RegistAPIView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = User.objects.create_user(username=username, password=password, is_active=False)
        code_obj = ConfirmationCode.objects.create(user=user)
        code_obj.generate_code()



        
        return Response(status=status.HTTP_201_CREATED, data={'user_id': user.id,"confirmation_code": code_obj.code})

class ConfirmAPIView(APIView):
    def post(self,request):
        serializer = UserConfirmSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            code = serializer.validated_data['code']
            
            user = User.objects.get(username=username)
            confirmation_code = ConfirmationCode.objects.get(user=user)

            if confirmation_code.code == code:
                user.is_active = True
                user.save()
                print(user.is_active) 


                confirmation_code.delete()

                return Response(
                    {"detail": "Пользователь успешно подтвержден."},
                    status=status.HTTP_200_OK
                )
            else:
                return Response({"detail": "Неверный код подтверждения."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)