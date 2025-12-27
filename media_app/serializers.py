from rest_framework import serializers
from .models import File, Tag, FileTag


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class FileTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileTag
        fields = '__all__'

