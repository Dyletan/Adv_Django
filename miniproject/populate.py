import requests

BASE_URL = "http://127.0.0.1:8000"

def register_user(username, password, role):
    url = f"{BASE_URL}/users/register/"
    data = {"username": username, "password": password, "role": role}
    response = requests.post(url, json=data)
    if response.status_code == 201:
        print(f"CustomUserUser '{username}' registered successfully.")
        return response.json()["user"]["id"]  # возвращает id пользователя
    else:
        print(f"CustomUserFailed to register user '{username}': {response.text}")
        return None

def login(username, password):
    url = f"{BASE_URL}/users/login/"
    data = {"username": username, "password": password}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print(f"CustomUserLogged in as '{username}'.")
        return response.json()["access"]
    else:
        print(f"CustomUserFailed to log in as '{username}': {response.text}")
        return None

def create_category(name, token):
    url = f"{BASE_URL}/products/categories/add/"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"name": name}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        print(f"CustomUserCategory '{name}' created successfully.")
        return response.json()["id"]
    else:
        print(f"CustomUserFailed to create category '{name}': {response.text}")
        return None

def create_product(name, category_id, price, seller_id, token, qty):
    url = f"{BASE_URL}/products/add/"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"name": name, "category": category_id, "price": price, "seller": seller_id, "quantity": qty}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        print(f"CustomUserProduct '{name}' created successfully.")
    else:
        print(f"CustomUserFailed to create product '{name}': {response.text}")

def main():
    # 1. Регистрируем пользователей:
    seller_id = register_user("seller1", "sellerpass", "trader")
    customer_id = register_user("customer1", "customerpass", "customer")
    sales_rep_id = register_user("sales1", "salesreppass", "sales_rep")
    
    # 2. Логинимся как админ (предполагается, что admin уже создан с именем 'dyletant' и паролем '123')
    admin_token = login("dyletant", "123")
    if not admin_token:
        print("CustomUserAdmin login failed. Cannot create categories.")
        return
    
    # 3. Создаем категории
    cat_electronics = create_category("Electronics", admin_token)
    cat_books = create_category("Books", admin_token)
    
    # 4. Логинимся как продавец (trader) для создания продуктов
    seller_token = login("seller1", "sellerpass")
    if not seller_token or not seller_id:
        print("CustomUserSeller login failed or seller id is missing. Cannot create products.")
        return
    
    # 5. Создаем продукты, если категории были успешно созданы
    if cat_electronics:
        create_product("Laptop", cat_electronics, 1200, seller_id, seller_token, 50)
    if cat_books:
        create_product("Python Book", cat_books, 50, seller_id, seller_token, 100)
    
    print("\nCustomUserDatabase populated successfully!")

if __name__ == "__main__":
    main()
