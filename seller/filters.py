import django_filters
from django_filters import DateFilter, CharFilter

from shop.models import *

class OrdersFilter(django_filters.FilterSet):
    Product = CharFilter(field_name="items_json", lookup_expr='icontains')
    class Meta:
        model = Orders
        # fields = ['seller','customer']
        fields = ['customer','order_id','amount','status','mode']
        # exclude = ['order_qr','items_json',]