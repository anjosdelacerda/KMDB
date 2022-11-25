from django.shortcuts import get_object_or_404
from ipdb import set_trace
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView, Request, Response, status

from .models import Movie
from .permissions import MovieCredentials
from .serializers import MovieSerializer


class MovieView(APIView, PageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [MovieCredentials]

    def post(self, request: Request) -> Response:
        serializer = MovieSerializer(data=request.data)

        create_movie = serializer.is_valid()

        if not create_movie:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)

    
    def get(self, request: Request) -> Response:
        movies = Movie.objects.all()

        if not movies:
            return Response({"detail": "movies not found."})

        result_page = self.paginate_queryset(movies, request, view=self)

        serializer = MovieSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)


class MovieGetIdView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [MovieCredentials]

    def get(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        serializer = MovieSerializer(movie)

        return Response(serializer.data)

    def patch(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        serializer = MovieSerializer(movie, request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
        except KeyError as error:
            return Response(*error.args)

        return Response(serializer.data)

    def delete(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        movie.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
