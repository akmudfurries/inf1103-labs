import json
from pathlib import Path

INVENTORY_FILE = Path(__file__).with_name("inventory.json")


def load_inventory():

    if INVENTORY_FILE.exists():
        print("inventory.json found.")
        try:
            with INVENTORY_FILE.open("r", encoding="utf-8") as file:
                inventory = json.load(file)

            if not isinstance(inventory, dict):
                raise ValueError("Inventory data must be a JSON object.")

            if not isinstance(inventory.get("products", []), list):
                raise ValueError("'products' must be a list.")

            inventory.setdefault("products", [])
            print("Inventory loaded successfully.")
            return inventory

        except (OSError, json.JSONDecodeError, ValueError) as error:
            print(f"Could not load inventory.json: {error}")
            print("Starting with empty inventory.")
    else:
        print("inventory.json not found. Starting with empty inventory.")

    return {"products": []}


def save_inventory(inventory):
    
    try:
        with INVENTORY_FILE.open("w", encoding="utf-8") as file:
            json.dump(inventory, file, indent=4)
        return True
    except OSError as error:
        print(f"Unable to save inventory: {error}")
        return False


def search_product(inventory, product_id):
    
    for product in inventory["products"]:
        if product["id"].casefold() == product_id.strip().casefold():
            return product
    return None


def display_all(inventory):

    print("Current Inventory")
    print("-" * 48)

    if not inventory["products"]:
        print("Inventory is empty.")

    for product in inventory["products"]:
        print(
            f"ID: {product['id']} | Name: {product['name']} | "
            f"Price: ${product['price']:.2f} | Stock: {product['stock']}"
        )

    print("-" * 48)


def add_product(inventory):

    print("Add New Product")
    product_id = input("Product ID: ").strip()

    if not product_id:
        print("Product ID cannot be empty.")
        return

    if search_product(inventory, product_id) is not None:
        print("A product with that ID already exists.")
        return

    name = input("Product Name: ").strip()
    if not name:
        print("Product name cannot be empty.")
        return

    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))

        if price < 0 or stock < 0:
            raise ValueError
    except ValueError:
        print("Enter a non-negative price and a non-negative whole-number stock quantity.")
        return

    product = {
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock
    }

    inventory["products"].append(product)
    print("Product added successfully!")


def update_stock(inventory):

    print("Update Stock")
    product_id = input("Enter Product ID: ").strip()
    product = search_product(inventory, product_id)

    if product is None:
        print("Product not found.")
        return

    print("Product Found:")
    print(f"Name: {product['name']}")
    print(f"Current Stock: {product['stock']}")

    try:
        new_stock = int(input("New Stock Quantity: "))
        if new_stock < 0:
            raise ValueError
    except ValueError:
        print("Stock must be a non-negative whole number.")
        return

    product["stock"] = new_stock
    print("Stock updated successfully!")


def search_and_display(inventory):

    print("Search Product")
    product_id = input("Enter Product ID: ").strip()
    product = search_product(inventory, product_id)

    if product is None:

        print("Product not found.")
        return

    print("Product Found")
    print("-" * 48)
    print(f"ID: {product['id']}")
    print(f"Name: {product['name']}")
    print(f"Price: ${product['price']:.2f}")
    print(f"Stock: {product['stock']}")
    print("-" * 48)


    def main():
        print("=" * 40)
        print("INVENTORY MANAGEMENT SYSTEM")
        print("=" * 40)

        inventory = load_inventory()

        while True:
            print("----------- MENU -----------")
            print("1. Display All Products")
            print("2. Add Product")
            print("3. Update Stock")
            print("4. Search Product")
            print("5. Save Inventory")
            print("6. Exit")
            print("----------------------------")

            option = input("Enter option: ").strip()

            if option == "1":
                display_all(inventory)

            elif option == "2":
                add_product(inventory)

            elif option == "3":
                update_stock(inventory)

            elif option == "4":
                search_and_display(inventory)

            elif option == "5":
                print("Saving inventory...")
                if save_inventory(inventory):
                    print("Inventory saved successfully to inventory.json.")

            elif option == "6":
                print("Saving inventory before exit...")
                if save_inventory(inventory):
                    print("Inventory saved successfully.")
                print("Thank you for using Inventory Management System.")
                print("Program terminated.")
                break

            else:
                print("Invalid option. Please enter a number from 1 to 6.")



    main()