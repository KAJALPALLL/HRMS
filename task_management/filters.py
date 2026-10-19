import django_filters
from . models import TaskManagement

class TaskFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(field_name='id',lookup_expr='icontains')

    class Meta:
        model = TaskManagement
        fields = ['id']

