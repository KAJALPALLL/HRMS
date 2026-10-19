from . models import Tickets

import django_filters



class TicketsFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(field_name='id',lookup_expr='icontains')
    class Meta:
        model = Tickets
        fields = ['id']
