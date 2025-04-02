from django.forms import ModelForm
from django import forms
from .models import Expense, GroupExpense, User

class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = ['name', 'amount', 'category']
        
class GroupExpenseForm(ModelForm):
    class Meta:
        model = GroupExpense
        fields = ['name', 'amount', 'users']

    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )