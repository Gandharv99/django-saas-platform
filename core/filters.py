import django_filters
from core.models import Task

class TaskFilter(django_filters.FilterSet):
    deadline_min = django_filters.DateFilter(field_name='deadline', lookup_expr='gte')
    deadline_max = django_filters.DateFilter(field_name='deadline', lookup_expr='lte')
    search = django_filters.CharFilter(field_name='search_task')
    class Meta:
        model = Task
        fields = ['project', 'assigned_to', 'status', 'priority']

    def search_task(self, queryset, name, value):
        return queryset.filter(title__icontains=value)