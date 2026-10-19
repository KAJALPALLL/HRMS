from .models import LeaveRequest
import django_filters
from user_management.models import Employee

class LeaveFilters(django_filters.FilterSet):
    employee__username = django_filters.CharFilter(field_name='employee__username',lookup_expr='icontains')

    class Meta:
        model = LeaveRequest
        fields = ('employee__username',)

