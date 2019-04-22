from rest_framework import generics
from .models import Songs
from .serializers import SongsSerializer, TokenSerializer
from rest_framework_jwt.settings import api_settings
from rest_framework import permissions, status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.views import Response


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class ListCreateSongsView(generics.ListCreateAPIView):
    """
    GET songs/
    POST songs/
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Songs.objects.all()
    serializer_class = SongsSerializer
    '''
    @validate_request_data
    def post(self, request, *args, **kwargs):
        a_song = Songs.objects.create(
            title=request.data["title"],
            artist=request.data["artist"]
        )
        return Response(
            data=SongsSerializer(a_song).data,
            status=status.HTTP_201_CREATED
        )
    '''

class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """

    # This permission class will over ride the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)
    serializer_class = TokenSerializer

    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response(serializer.data)
        return Response({'message' : 'Invalid Credentials'},status=status.HTTP_401_UNAUTHORIZED)