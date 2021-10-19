from rest_framework import serializers


class ResultSerializer(serializers.Serializer):
    message = serializers.CharField()
    resp = serializers.ListField()
    error = serializers.BooleanField()


class ResultDicSerializer(serializers.Serializer):
    message = serializers.CharField()
    resp = serializers.DictField()
    error = serializers.BooleanField()


class ErrorSerializer(serializers.Serializer):
    message = serializers.CharField()
    error = serializers.BooleanField()

