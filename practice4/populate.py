import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "n_counter.settings")
django.setup()

from app.models import Food

def populate_foods():
    food_items = [
        {'name': 'Apple', 'carbs': 25, 'fats': 0.3, 'proteins': 0.5, 'calorie': 95},
        {'name': 'Banana', 'carbs': 27, 'fats': 0.3, 'proteins': 1.3, 'calorie': 105},
        {'name': 'Chicken Breast', 'carbs': 0, 'fats': 3.6, 'proteins': 31, 'calorie': 165},
        {'name': 'Rice', 'carbs': 45, 'fats': 0.4, 'proteins': 4.3, 'calorie': 206},
        {'name': 'Egg', 'carbs': 1.1, 'fats': 5, 'proteins': 6, 'calorie': 68},
        {'name': 'Salmon', 'carbs': 0, 'fats': 13, 'proteins': 20, 'calorie': 208},
    ]

    for food in food_items:
        Food.objects.get_or_create(**food)

    print("Successfully populated Food model!")

if __name__ == "__main__":
    populate_foods()