import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def login(role, username, password):
    url = f"{BASE_URL}/users/login/"
    data = {"username": username, "password": password}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        tokens = response.json()  # expects keys "access" and "refresh"
        print(f"Logged in as {role} ({username}).")
        return tokens
    else:
        print("Login failed:", response.text)
        return None

def logout(token, refresh_token):
    url = f"{BASE_URL}/users/logout/"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"refresh": refresh_token}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print("Logged out successfully.")
    elif response.json().get("error") == "Invalid token":
        print("Token already invalidated; logged out.")
    else:
        print("Logout failed:", response.text)

def get_profile(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/users/profile/", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch profile:", response.text)
        return None

# CUSTOMER FUNCTIONS
def list_products(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/products/", headers=headers)
    if response.status_code == 200:
        products = response.json()
        print("Product List:")
        if products:
            for prod in products:
                print(f"ID: {prod.get('id')}, Name: {prod.get('name')}, Price: {prod.get('price')}, Quantity: {prod.get('quantity', 'N/A')}")
        else:
            print("No products available.")
    else:
        print("Failed to fetch products:", response.text)

def place_order(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/products/", headers=headers)
    if response.status_code != 200:
        print("Failed to fetch products:", response.text)
        return
    products = response.json()
    if not products:
        print("No products available.")
        return
    print("Available products:")
    for prod in products:
        print(f"ID: {prod.get('id')}, Name: {prod.get('name')}, Price: {prod.get('price')}, Quantity: {prod.get('quantity', 'N/A')}")
    product_id = input("Enter product ID to order: ").strip()
    order_quantity = input("Enter order quantity: ").strip()
    price = None
    for prod in products:
        if str(prod.get("id")) == product_id:
            price = prod.get("price")
            break
    if price is None:
        print("Invalid product ID.")
        return
    order_data = {
        "order_type": "buy",
        "quantity": order_quantity,
        "price": price
    }
    order_response = requests.post(f"{BASE_URL}/trading/orders/create/{product_id}/", headers=headers, json=order_data)
    if order_response.status_code in [200, 201]:
        print("Order placed:", order_response.json())
    else:
        print("Failed to place order:", order_response.text)

def view_invoices(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/sales/invoices/", headers=headers)
    if response.status_code == 200:
        invoices = response.json()
        print("Your Invoices:")
        print(json.dumps(invoices, indent=2))
    else:
        print("Failed to fetch invoices:", response.text)

def pay_invoice(token):
    headers = {"Authorization": f"Bearer {token}"}
    invoice_id = input("Enter Invoice ID to pay: ").strip()
    response = requests.post(f"{BASE_URL}/sales/invoices/{invoice_id}/pay/", headers=headers)
    if response.status_code in [200, 201]:
        print("Invoice paid successfully:", response.json())
    else:
        print("Failed to pay invoice:", response.text)

def view_sales_orders_customer(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/sales/", headers=headers)
    if response.status_code == 200:
        orders = response.json()
        print("Your SalesOrders:")
        print(json.dumps(orders, indent=2))
    else:
        print("Failed to fetch SalesOrders:", response.text)

# TRADER FUNCTIONS (in addition to Customer functions)
def create_product(token, seller_id):
    headers = {"Authorization": f"Bearer {token}"}
    name = input("Enter new product name: ").strip()
    category = input("Enter category ID for the product: ").strip()
    price = input("Enter product price: ").strip()
    quantity = input("Enter product quantity: ").strip()
    description = input("Enter product descritpion: ").strip()
    product_data = {
        "name": name,
        "category": category,
        "price": price,
        "quantity": quantity,
        "seller": seller_id,
        "description": description
    }
    response = requests.post(f"{BASE_URL}/products/add/", json=product_data, headers=headers)
    if response.status_code in [200, 201]:
        print("Product created:", json.dumps(response.json(), indent=2))
    else:
        print("Failed to create product:", response.text)

# SALES REPRESENTATIVE FUNCTIONS
def list_pending_transactions(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/trading/transactions/", headers=headers)
    if response.status_code == 200:
        transactions = response.json()
        print("Pending Transactions:")
        print(json.dumps(transactions, indent=2))
    else:
        print("Failed to fetch transactions:", response.text)

def approve_transaction(token):
    headers = {"Authorization": f"Bearer {token}"}
    trans_id = input("Enter transaction ID to approve: ").strip()
    # Approve the transaction
    response = requests.post(f"{BASE_URL}/trading/transactions/{trans_id}/approve/", headers=headers)
    if response.status_code in [200, 201]:
        result = response.json()
        print("Transaction approved.", result)
        # Check if the SalesOrder and Invoice were returned automatically
        if "sales_order" not in result:
            # If not, call the endpoint to create a SalesOrder from the approved transaction
            so_response = requests.post(f"{BASE_URL}/sales/create/{trans_id}/", headers=headers)
            if so_response.status_code in [200, 201]:
                sales_order = so_response.json().get("sales_order")
                print("SalesOrder created:", sales_order)
                # Now generate an Invoice for the SalesOrder
                inv_response = requests.post(
                    f"{BASE_URL}/sales/{sales_order['id']}/generate_invoice/",
                    headers=headers,
                    json={"due_date": "2025-12-31"}
                )
                if inv_response.status_code in [200, 201]:
                    print("Invoice generated:", inv_response.json())
                else:
                    print("Failed to generate invoice:", inv_response.text)
            else:
                print("Failed to create SalesOrder:", so_response.text)
    else:
        print("Failed to approve transaction:", response.text)

def reject_transaction(token):
    headers = {"Authorization": f"Bearer {token}"}
    trans_id = input("Enter transaction ID to reject: ").strip()
    response = requests.post(f"{BASE_URL}/trading/transactions/{trans_id}/cancel/", headers=headers)
    if response.status_code in [200, 201]:
        print("Transaction rejected.", response.json())
    else:
        print("Failed to reject transaction:", response.text)

def list_sales_orders_sales_rep(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/sales/", headers=headers)
    if response.status_code == 200:
        orders = response.json()
        print("SalesOrders:")
        print(json.dumps(orders, indent=2))
    else:
        print("Failed to fetch SalesOrders:", response.text)

def main():
    current_token = None
    current_refresh = None
    current_role = None
    current_username = None

    while True:
        if not current_token:
            print("\nSelect role to login:")
            print("1. Customer")
            print("2. Trader")
            print("3. Sales Representative")
            print("4. Exit")
            choice = input("Enter your choice: ").strip()
            if choice == "4":
                break
            if choice == "1":
                current_role = "customer"
                current_username = "customer1"
                password = "customerpass"
            elif choice == "2":
                current_role = "trader"
                current_username = "seller1"
                password = "sellerpass"
            elif choice == "3":
                current_role = "sales_rep"
                current_username = "sales1"
                password = "salesreppass"
            else:
                print("Invalid choice.")
                continue
            tokens = login(current_role, current_username, password)
            if tokens:
                current_token = tokens.get("access")
                current_refresh = tokens.get("refresh")
            else:
                continue

        print(f"\nCurrent role: {current_role} ({current_username})")
        print("Select an action:")
        if current_role == "customer":
            print("1. View all products")
            print("2. Place an order for a product")
            print("3. View my invoices")
            print("4. Pay an invoice")
            print("5. View my SalesOrders")
        elif current_role == "trader":
            print("1. Create a new product")
            print("2. View all products")
            print("3. Place an order for a product")
            print("4. View my invoices")
            print("5. Pay an invoice")
            print("6. View my SalesOrders")
        elif current_role == "sales_rep":
            print("1. View all pending transactions")
            print("2. Approve a transaction")
            print("3. Reject a transaction")
            print("4. View all SalesOrders")
        print("9. Logout")
        print("0. Exit")
        action = input("Enter your choice: ").strip()
        if action == "9":
            logout(current_token, current_refresh)
            current_token = None
            current_refresh = None
            current_role = None
            current_username = None
            print("Logged out.\n")
            continue
        if action == "0":
            break

        if current_role == "customer":
            if action == "1":
                list_products(current_token)
            elif action == "2":
                place_order(current_token)
            elif action == "3":
                view_invoices(current_token)
            elif action == "4":
                pay_invoice(current_token)
            elif action == "5":
                response = requests.get(f"{BASE_URL}/sales/", headers={"Authorization": f"Bearer {current_token}"})
                print("My SalesOrders:", json.dumps(response.json(), indent=2))
            else:
                print("Invalid action.")
        elif current_role == "trader":
            if action == "1":
                profile = get_profile(current_token)
                if profile:
                    seller_id = profile.get("id")
                    create_product(current_token, seller_id)
            elif action == "2":
                list_products(current_token)
            elif action == "3":
                place_order(current_token)
            elif action == "4":
                view_invoices(current_token)
            elif action == "5":
                pay_invoice(current_token)
            elif action == "6":
                response = requests.get(f"{BASE_URL}/sales/", headers={"Authorization": f"Bearer {current_token}"})
                print("My SalesOrders:", json.dumps(response.json(), indent=2))
            else:
                print("Invalid action.")
        elif current_role == "sales_rep":
            if action == "1":
                list_pending_transactions(current_token)
            elif action == "2":
                approve_transaction(current_token)
            elif action == "3":
                reject_transaction(current_token)
            elif action == "4":
                list_sales_orders_sales_rep(current_token)
            else:
                print("Invalid action.")

    print("Exiting demo.")

if __name__ == "__main__":
    main()
