from rest_framework import serializers
from .models import Orders, Contact, OrderUpdate

class AllOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'