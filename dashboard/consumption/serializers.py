from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserSummarySerializer(serializers.Serializer):
    pk = serializers.CharField(max_length=200)
    tariff_code = serializers.CharField(max_length=200)
    area_code = serializers.CharField(max_length=200)
    average = serializers.FloatField()
    total = serializers.FloatField()


class AreaSummarySerializer(serializers.Serializer):
    area_code = serializers.CharField(max_length=200)
    average = serializers.FloatField()
    total = serializers.FloatField()
