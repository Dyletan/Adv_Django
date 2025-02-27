from django.shortcuts import render, redirect
from .models import Food, Consume, HealthGoal 
from django.http import JsonResponse
from .forms import FoodForm, HealthGoalForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from datetime import timedelta, date


@login_required
def index(request):
    if request.method =="POST":
        food_consumed = request.POST['food_consumed']
        c = Food.objects.get(name=food_consumed)
        user = request.user
        consume = Consume(user=user, food_consumed=c)
        consume.save()
        foods = Food.objects.all()
    else:
        foods = Food.objects.all()
    consumed_food = Consume.objects.filter(user=request.user)
    return render(request, 'app/index.html', {'foods': foods, 'consumed_food':consumed_food})

@login_required
def delete_consume(request, id):
    consumed_food = Consume.objects.get(id=id)
    if request.method=="POST":
        consumed_food.delete()
        return redirect('/')
    return render(request, 'app/delete.html')

@login_required
def nutrient_summary_data(request):
  consumed = Consume.objects.filter(user=request.user)
  goal, created = HealthGoal.objects.get_or_create(user=request.user)
  data = {
    "carbs": sum(c.food_consumed.carbs for c in consumed),
    "proteins": sum(c.food_consumed.proteins for c in consumed),
    "fats": sum(c.food_consumed.fats for c in consumed),
    "calories": sum(c.food_consumed.calorie for c in consumed),
    "goal_calories": goal.daily_calorie_goal,
    "goal_carbs": goal.carb_goal,
    "goal_proteins": goal.protein_goal,
    "goal_fats": goal.fat_goal,
  }
  return JsonResponse(data)

@login_required
def chart_data(request):
    consumed = Consume.objects.filter(user=request.user)
    goal, _ = HealthGoal.objects.get_or_create(user=request.user) # Get or create HealthGoal
    data = {
        "labels": [c.food_consumed.name for c in consumed],
        "carbs": [c.food_consumed.carbs for c in consumed],
        "proteins": [c.food_consumed.proteins for c in consumed],
        "fats": [c.food_consumed.fats for c in consumed],
        "calories": [c.food_consumed.calorie for c in consumed],
        "goal_carbs": goal.carb_goal, # Add goal data to response
        "goal_proteins": goal.protein_goal,
        "goal_fats": goal.fat_goal,
        "goal_calories": goal.daily_calorie_goal,
    }
    return JsonResponse(data)

@login_required
def line_chart_data(request):
    today = date.today()
    labels = []
    daily_calories = []

    for i in range(7): 
        current_date = today - timedelta(days=i)
        labels.append(current_date.strftime("%Y-%m-%d"))
        # Replace 'date_consumed' with the CORRECT field name from your model (e.g., 'date')
        daily_consumption = Consume.objects.filter(user=request.user, date=current_date) # Changed to 'date'
        total_calories = sum(c.food_consumed.calorie for c in daily_consumption)
        daily_calories.append(total_calories)

    labels.reverse()
    daily_calories.reverse()

    data = {
        "labels": labels,
        "calories": daily_calories,
    }
    return JsonResponse(data)

@login_required
def update_goals(request):
    goal, created = HealthGoal.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = HealthGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = HealthGoalForm(instance=goal)
    return render(request, "app/update_goals.html", {"form": form})

@login_required
def add_food(request):
    if request.method == "POST":
        form = FoodForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = FoodForm()
    return render(request, "app/add_food.html", {"form": form})

def register(request):
      if request.method == "POST":
          form = UserCreationForm(request.POST)
          if form.is_valid():
              form.save()
              return redirect("login")
      else:
          form = UserCreationForm()
      return render(request, "app/register.html", {"form": form})