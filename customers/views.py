from rest_framework.views import APIView
from rest_framework.response import Response
from customers.models import Customer
from .serializers import CustomerFullSerializer

class AllCustomersView(APIView):
    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerFullSerializer(customers, many=True)
        return Response(serializer.data)

