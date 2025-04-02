import django_filters
from django_filters.widgets import DateRangeWidget
from .models import Expense, Category

class ExpenseFilter(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter(
        widget=DateRangeWidget(attrs={'type': 'date'})
    )
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.none())

    class Meta:
        model = Expense
        fields = ['date', 'category']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.filters['category'].queryset = Category.objects.filter(user=user)
