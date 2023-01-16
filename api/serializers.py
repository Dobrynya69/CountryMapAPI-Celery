from rest_framework import serializers
from .models import *


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('name', 'population')


class ReviewSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = Review
        fields = ('slug', 'title', 'author_id', 'country', 'text', 'image')
