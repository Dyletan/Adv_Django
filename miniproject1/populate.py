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
    print("Creating users")
      
    # Create Admin user
    admin_user, created = User.objects.get_or_create(username='admin', defaults={
        'password':'adminpassword',
        'email':'admin@example.com',
        'role':'admin',
        'first_name':'Admin',
        'last_name':'User'
    })
    if created:
        admin_user.set_password('adminpassword')
        admin_user.save()
        print(f"Admin user '{admin_user.username}' created.")
    else:
        print(f"Admin user '{admin_user.username}' already exists.")

    # Create Trader user
    trader_user, created = User.objects.get_or_create(
        username='trader1',
        defaults={
            'password':'traderpassword',
            'email':'trader1@example.com',
            'role':'trader',
            'first_name':'Trader',
            'last_name':'One'
        })
    if created:
        trader_user.set_password('traderpassword')
        trader_user.save()
        print(f"Trader user '{trader_user.username}' created.")
    else:
        print(f"Trader user '{trader_user.username}' already exists.")


    # Create Customer user
    customer_user, created = User.objects.get_or_create(
        username='customer1',
        defaults={
            'password':'customerpassword',
            'email':'customer1@example.com',
            'role':'customer',
            'first_name':'Customer',
            'last_name':'One'
        })
    if created:
        customer_user.set_password('customerpassword')
        customer_user.save()
        print(f"Customer user '{customer_user.username}' created.")
    else:
        print(f"Customer user '{customer_user.username}' already exists.")

    # --- Product Categories and Products ---
    print("Creating product categories and products")
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

    # --- Trading Orders ---
    print("Creating trading orders...")

    trader = User.objects.get(username='trader1')
    customer = User.objects.get(username='customer1')
    laptop_product = Product.objects.get(name='Laptop')
    smartphone_product = Product.objects.get(name='Smartphone')

    order = Order.objects.create(
        user=trader,
        product=laptop_product,
        order_type='buy',
        quantity=5,
        price=1200.00,
        status='pending'
    )

    print(f"Trading Order '{order.id}' created for '{trader.username}'.")

    order2 = Order.objects.create(
        user=customer,
        product=smartphone_product,
        order_type='sell',
        quantity=10,
        price=900.00,
        status='completed'
    )
    print(f"Trading Order '{order2.id}' created for '{customer.username}'.")
    print("Trading orders created.")

    # --- Sales Orders and Sales Order Items ---
    print("Creating sales orders and sales order items...")
    # Get users and products (assuming they exist)
    customer_user_sales = User.objects.get(username='customer1')
    trader_user = User.objects.get(username='trader1', role='trader')
    tshirt_product = Product.objects.get(name='T-Shirt')
    laptop_product = Product.objects.get(name='Laptop')

    sales_order1 = SalesOrder.objects.create(
        seller=trader_user,
        customer=customer_user_sales,
        status='pending',
        discount_percent=5.0,
        notes='First sales order for customer1'
    )
    print(f"Sales Order '{sales_order1.id}' created for customer '{customer_user_sales.username}'.")

    sales_order_item1 = SalesOrderItem.objects.create(
        sales_order=sales_order1,
        product=tshirt_product,
        quantity=2,
        unit_price=25.00
    )
    print(f"Sales Order Item '{sales_order_item1.id}' created for Sales Order '{sales_order1.id}'.")

    sales_order_item2 = SalesOrderItem.objects.create(
        sales_order=sales_order1,
        product=laptop_product,
        quantity=1,
        unit_price=1200.00
    )
    print(f"Sales Order Item '{sales_order_item2.id}' created for Sales Order '{sales_order1.id}'.")
    
    print("Database population complete.")


if __name__ == '__main__':
    populate_data()