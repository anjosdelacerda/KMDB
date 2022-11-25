from genres.models import Genre
from genres.serializers import GenreSerializer
from ipdb import set_trace
from rest_framework import serializers

from .models import Movie


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10)
    premiere = serializers.DateField()
    classification = serializers.IntegerField()
    synopsis = serializers.CharField()

    genres = GenreSerializer(many=True)

    def create(self, validated_data: dict) -> Movie:
        genre_data = validated_data.pop("genres")

        movie = Movie.objects.create(**validated_data)

        for create_genre in genre_data:
            genre, _ = Genre.objects.get_or_create(**create_genre)
            movie.genres.add(genre)

        return movie

    def update(self, instance: Movie, validated_data: dict) -> Movie:
        genre_data = validated_data.pop("genres", None)

        if genre_data:
            instance.genres.set([])
            for create_genre in genre_data:
                genre, _ = Genre.objects.get_or_create(**create_genre)
                instance.genres.add(genre)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
