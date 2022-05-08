from rest_framework import serializers
from .models import Model, File

class ModelFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = '__all__'


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
