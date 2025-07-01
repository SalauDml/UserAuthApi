from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.

class RegView(APIView):
    """
    post:
    Used for User Registration
    Username, password, First name, Last name and email are the expected and required fields.
    Expected JSON:
    {
    "first_name": "firstname",
    "last_name":"last_name",
    "username":"username",
    "password":"password",
    "email":"email"
    }
    """
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['first_name', 'last_name', 'username', 'password', 'email'],
            properties={
                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format='password'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, format='email'),
            },
        )
    )
    def post(self,request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("User created",status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
class LoginView(APIView):

    """
    post:
    Used for user login. 
    User must enter username and password. Other fields are optional
    Returns access token that expires every 60 minutes.
    Expected JSON
    {
    "username": "username",
    "password":"password"
    }    
    """
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format='password'),
            },
        )
    )
    def post(self,request):
        try:
            username = request.data.get('username') 
            password = request.data.get('password')

            if username is None or password is None :
                raise ValueError("Username and password are required")
            
            user = authenticate(username = username, password = password)

            if user is not None:
                token = AccessToken.for_user(user)
                return Response({"Access Token":str(token)},status=status.HTTP_202_ACCEPTED)
            else:
                return Response("Invalid Credentials",status=status.HTTP_401_UNAUTHORIZED)
        except ValueError as ve:
            return Response({"error":ve},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response("Something went wrong",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ProfileView(APIView):
    """
    get:
        Used to get the profile of logged in User
        Returns complete profile of logged in User when Token is added in Bearers section of request.
        Protected route i.e will not work without being logged in.    
    """

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <access_token>",
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    def get (self,request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)

