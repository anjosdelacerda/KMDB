from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from ipdb import set_trace
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView, Request, Response, status

from .models import User
from .permissions import IsUserAdm, IsUserCritic
from .serializers import LoginSerializer, UserSerializer


class UserView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)

        if not user:
            return Response({'detail': 'invalid username / password'}, status.HTTP_403_FORBIDDEN)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({'token': token.key})


class UserGetListView(APIView, PageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsUserAdm]

    def get(self, request: Request) -> Response:
        users = User.objects.all()

        if not users:
            return Response({"detail": "Users if not exists."}, status.HTTP_404_NOT_FOUND)

        result_page = self.paginate_queryset(users, request, view=self)

        serializer = UserSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)


class UserGetIdView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsUserAdm | IsUserCritic]

    def get(self, request: Request, user_id: int) -> Response:
        user = get_object_or_404(User, id=user_id)

        self.check_object_permissions(request, user)

        serializer = UserSerializer(user)

        return Response(serializer.data)
