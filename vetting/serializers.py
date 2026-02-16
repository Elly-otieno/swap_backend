from rest_framework import serializers

class PrimarySerializer(serializers.Serializer):
    session_id = serializers.IntegerField()
    full_name = serializers.CharField()
    id_number = serializers.CharField()
    yob = serializers.IntegerField()


class SecondarySerializer(serializers.Serializer):
    session_id = serializers.IntegerField()
    answers = serializers.JSONField()
