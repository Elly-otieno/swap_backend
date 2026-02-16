from rest_framework import serializers
from swap.utils.msisdn import normalize_msisdn, InvalidMSISDN

class StartSwapSerializer(serializers.Serializer):
    msisdn = serializers.CharField()

    def validate_msisdn(self, value):
        try:
            return normalize_msisdn(value)
        except InvalidMSISDN as e:
            raise serializers.ValidationError(str(e))

