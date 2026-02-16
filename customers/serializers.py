from rest_framework import serializers
from customers.models import Customer
from lines.models import Line
from wallet.models import WalletProfile


class LineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Line
        fields = "__all__"


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletProfile
        fields = "__all__"


class CustomerFullSerializer(serializers.ModelSerializer):
    line = serializers.SerializerMethodField()
    wallet = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = "__all__"

    def get_line(self, obj):
        line = Line.objects.filter(customer=obj).first()
        if line:
            return LineSerializer(line).data
        return None

    def get_wallet(self, obj):
        wallet = WalletProfile.objects.filter(customer=obj).first()
        if wallet:
            return WalletSerializer(wallet).data
        return None
