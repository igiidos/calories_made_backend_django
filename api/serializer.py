from rest_framework import serializers


class ResultSerializer(serializers.Serializer):
    message = serializers.CharField()
    resp = serializers.ListField()
    error = serializers.BooleanField()