from django.shortcuts import get_object_or_404
from ipdb import set_trace
from movies.models import Movie
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView, Request, Response, status

from .models import Review
from .permissions import ReviewCredentials, ReviewIdCredentials
from .serializers import ReviewSerializer


class ReviewView(APIView, PageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [ReviewCredentials]

    def post(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)
        review_already_exist = Review.objects.filter(
            movie_id=movie.id, critic=request.user.id).exists()
        
        
        serializer = ReviewSerializer(data=request.data)

        #a ordem que estava dando problema

        if review_already_exist:
            return Response({"detail": "Review already exists."}, status.HTTP_403_FORBIDDEN)


        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        serializer.save(movie=movie, critic=request.user)

        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, request: Request, movie_id: int) -> Response:
        reviews = Review.objects.filter(movie_id=movie_id)

        if not reviews:
            return Response({"detail": "Reviews Not found."}, status.HTTP_404_NOT_FOUND)

        result_page = self.paginate_queryset(reviews, request, view=self)

        serializer = ReviewSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)


class ReviewGetIdView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [ReviewCredentials, ReviewIdCredentials]

    def get(self, request: Request, movie_id: int, review_id: int) -> Response:
        review = get_object_or_404(Review, id=review_id, movie_id=movie_id)

        serializer = ReviewSerializer(review)

        return Response(serializer.data)

    def delete(self, request: Request, movie_id: int, review_id: int) -> Response:
        review = get_object_or_404(Review, id=review_id, movie_id=movie_id)
        self.check_object_permissions(request, review.critic)

        review.delete()

        return Response({}, status.HTTP_204_NO_CONTENT)
