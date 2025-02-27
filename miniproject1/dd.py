import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sales_trading_app.settings')
django.setup()

from users.models import User
from products.models import Category, Product
from trading.models import Order
from sales.models import SalesOrder, SalesOrderItem

def populate_data():
    print("Populating database...")

    # --- Users ---
    print("Creating users (using get_or_create)...")
      
    # Create Admin user
    admin_user, created = User.objects.get_or_create(username='admin', defaults={'password':'adminpassword', 'email':'admin@example.com', 'role':'admin', 'first_name':'Admin', 'last_name':'User'})
    if created:
        admin_user.set_password('adminpassword')
        admin_user.save()
        print(f"Admin user '{admin_user.username}' created.")
    else:
        print(f"Admin user '{admin_user.username}' already exists.")

    # Create Trader user
    trader_user, created = User.objects.get_or_create(username='trader1', defaults={'password':'traderpassword', 'email':'trader1@example.com', 'role':'trader', 'first_name':'Trader', 'last_name':'One'})
    if created:
        trader_user.set_password('traderpassword')
        trader_user.save()
        print(f"Trader user '{trader_user.username}' created.")
    else:
        print(f"Trader user '{trader_user.username}' already exists.")

    # Create Sales Representative user
    sales_rep_user, created = User.objects.get_or_create(username='salesrep1', defaults={'password':'salesreppassword', 'email':'salesrep1@example.com', 'role':'sales_representative', 'first_name':'SalesRep', 'last_name':'One'})
    if created:
        sales_rep_user.set_password('salesreppassword')
        sales_rep_user.save()
        print(f"Sales Representative user '{sales_rep_user.username}' created.")
    else:
        print(f"Sales Representative user '{sales_rep_user.username}' already exists.")

    # Create Customer user
    customer_user, created = User.objects.get_or_create(username='customer1', defaults={'password':'customerpassword', 'email':'customer1@example.com', 'role':'customer', 'first_name':'Customer', 'last_name':'One'})
    if created:
        customer_user.set_password('customerpassword')
        customer_user.save()
        print(f"Customer user '{customer_user.username}' created.")
    else:
        print(f"Customer user '{customer_user.username}' already exists.")
    print("Users checked and/or created.")

    # --- Product Categories and Products ---
    print("Creating product categories and products (using get_or_create)...")
    # Create Product Categories
    category_electronics, created = Category.objects.get_or_create(name='Electronics', defaults={'description':'Electronic gadgets and devices'})
    if created:
        print("Product category 'Electronics' created.")
    else:
        print("Product category 'Electronics' already exists.")

    category_clothing, created = Category.objects.get_or_create(name='Clothing', defaults={'description':'Apparel and fashion items'})
    if created:
        print("Product category 'Clothing' created.")
    else:
        print("Product category 'Clothing' already exists.")
    print("Product categories checked and/or created.")

    # Create Products (using get_or_create)...
    product1, created = Product.objects.get_or_create(
        name='Laptop',
        defaults={
            'description':'High-performance laptop for professionals',
            'category':category_electronics,
            'price':1200.00,
            'stock_quantity':50
        }
    )
    if created:
        print(f"Product '{product1.name}' created.")
    else:
        print(f"Product '{product1.name}' already exists.")

    product2, created = Product.objects.get_or_create(
        name='Smartphone',
        defaults={
            'description':'Latest smartphone with advanced features',
            'category':category_electronics,
            'price':900.00,
            'stock_quantity':100
        }
    )
    if created:
        print(f"Product '{product2.name}' created.")
    else:
        print(f"Product '{product2.name}' already exists.")

    product3, created = Product.objects.get_or_create(
        name='T-Shirt',
        defaults={
            'description':'Comfortable cotton t-shirt',
            'category':category_clothing,
            'price':25.00,
            'stock_quantity':200
        }
    )
    if created:
        print(f"Product '{product3.name}' created.")
    else:
        print(f"Product '{product3.name}' already exists.")
    print("Products checked and/or created.")


    # --- Trading Orders ---
    print("Creating trading orders...")
    # Get users and products (assuming they exist)
    trader = User.objects.filter(username='trader1', role='trader').first()
    customer = User.objects.filter(username='customer1', role='customer').first()
    laptop_product = Product.objects.filter(name='Laptop').first()
    smartphone_product = Product.objects.filter(name='Smartphone').first()

    # Отладочные принты
    print(f"Trader: {trader} (ID: {trader.id if trader else 'None'})")
    print(f"Laptop: {laptop_product} (ID: {laptop_product.id if laptop_product else 'None'})")

    # Проверка наличия объектов
    if not trader:
        raise ValueError("Trader user 'trader1' not found in database.")
    if not laptop_product:
        raise ValueError("Product 'Laptop' not found in database.")

    # Создаём заказ, если всё в порядке
    order = Order.objects.create(
        user=trader,
        product=laptop_product,
        order_type='buy',
        quantity=5,
        price=1200.00,
        status='pending'
    )

    print(f"Trading Order '{order.id}' created for '{trader.username}'.")

if __name__ == '__main__':
    populate_data()