from time import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ExpenseForm, GroupExpenseForm
from .models import Expense, Category, GroupExpense
from django.db.models import Sum, Q
import datetime
from .filters import ExpenseFilter
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import JsonResponse


@login_required(login_url="login")
def index(request):
    if request.method == "POST":
        expense_form = ExpenseForm(request.POST)
        if expense_form.is_valid():
            expense = expense_form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('index')
    else:
        expense_form = ExpenseForm()

    expenses_qs = Expense.objects.filter(user=request.user)
    expense_filter = ExpenseFilter(request.GET, queryset=expenses_qs, user=request.user)

    expenses = expense_filter.qs

    date_today = datetime.date.today()
    last_year = date_today - datetime.timedelta(days=365)
    last_month = date_today - datetime.timedelta(days=30)
    last_week = date_today - datetime.timedelta(days=7)

    sums = expenses.aggregate(
        total_expenses=Sum('amount'),
        yearly_sum=Sum('amount', filter=Q(date__gt=last_year)),
        monthly_sum=Sum('amount', filter=Q(date__gt=last_month)),
        weekly_sum=Sum('amount', filter=Q(date__gt=last_week))
    )

    daily_sums = expenses.values('date').order_by('date').annotate(sum=Sum('amount'))
    categorical_sums = expenses.values("category__name").order_by("category__name").annotate(sum=Sum("amount"))
    
    categories = Category.objects.filter(user=request.user)
    
    print("Aggregated sums:", sums)
    print("Total sums:", sums['total_expenses'])
    print("Categorical sums:", categorical_sums)
    

    return render(
        request, 'myapp/index.html',
        {
            'expense_form': expense_form,
            'expenses': expenses,
            'expense_filter': expense_filter,
            'total_expenses': sums['total_expenses'],
            'yearly_sum': sums['yearly_sum'],
            'monthly_sum': sums['monthly_sum'],
            'weekly_sum': sums['weekly_sum'],
            'daily_sums': daily_sums,
            'categorical_sums': categorical_sums,
            'categories': categories,
        }
    )

 
@login_required    
def edit(request, id): 
    expense = Expense.objects.get(id=id)
    expense_form = ExpenseForm(instance=expense)
    
    if request.method =="POST":
        expense = Expense.objects.get(id=id)
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request, 'myapp/edit.html', {'expense_form':expense_form})

@login_required
def delete(request, id):
    if request.method == "POST" and 'delete' in request.POST:
        expense= Expense.objects.get(id=id)
        expense.delete()
    return redirect('index') 

@login_required
def add_category(request):
    if request.method == 'POST':
        name = request.POST['name']
        Category.objects.create(name=name, user=request.user)
        return redirect('add_category')

    return render(request, 'myapp/add_category.html')


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = UserCreationForm()
    return render(request, "myapp/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("index")  # Redirect to homepage after login
    else:
        form = AuthenticationForm()
    return render(request, "myapp/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def create_group_expense(request):
    if request.method == 'POST':
        form = GroupExpenseForm(request.POST)
        if form.is_valid():
            group_expense = form.save(commit=False)
            group_expense.save()

            group_expense.create_user_shares()

            return redirect('index')
    else:
        form = GroupExpenseForm()

    return render(request, 'myapp/create_group_expense.html', {'form': form})

@login_required
def group_expenses_list(request):
    group_expenses = GroupExpense.objects.all()
    return render(request, 'myapp/group_expenses_list.html', {'group_expenses': group_expenses})