import json
from pathlib import Path

from inventory import Inventory
from product import Product

INVENTORY_FILE = Path(__file__).with_name("inventory.json")


# Handling file
def load_inventory():
    inventory = Inventory()

    if not INVENTORY_FILE.exists():
        print("inventory.json not found. Starting with empty inventory.")
        return inventory

    print("inventory.json found.")
    try:
        with INVENTORY_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("Inventory data must be a JSON object.")
        if not isinstance(data.get("products", []), list):
            raise ValueError("'products' must be a list.")

        for item in data.get("products", []):
            try:
                inventory.add_product(Product.from_dict(item))
            except (KeyError, TypeError, ValueError) as error:
                print(f"Skipping invalid product entry: {error}")

        print("Inventory loaded successfully.")

    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Could not load inventory.json: {error}")
        print("Starting with empty inventory.")
        return Inventory()

    return inventory


def save_inventory(inventory):
    try:
        with INVENTORY_FILE.open("w", encoding="utf-8") as file:
            json.dump(inventory.to_dict(), file, indent=4)
        return True
    except OSError as error:
        print(f"Unable to save inventory: {error}")
        return False


# ---------------- Menu actions (user input) ----------------
def add_product(inventory):
    print("Add New Product")

    product_id = input("Product ID: ").strip()
    if not product_id:
        print("Product ID cannot be empty.")
        return

    if inventory.search_product(product_id) is not None:
        print("A product with that ID already exists.")
        return

    name = input("Product Name: ").strip()
    if not name:
        print("Product name cannot be empty.")
        return

    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
        product = Product(product_id, name, price, stock)
    except ValueError:
        print(
            "Enter a non-negative price and a "
            "non-negative whole-number stock quantity."
        )
        return

    inventory.add_product(product)
    print("Product added successfully!")


def update_stock(inventory):
    print("Update Stock")

    product = inventory.search_product(input("Enter Product ID: "))
    if product is None:
        print("Product not found.")
        return

    print("Product Found:")
    print(f"Name: {product.name}")
    print(f"Current Stock: {product.stock}")

    try:
        product.update_stock(int(input("New Stock Quantity: ")))
    except ValueError:
        print("Stock must be a non-negative whole number.")
        return

    print("Stock updated successfully!")


def search_and_display(inventory):
    print("Search Product")

    product = inventory.search_product(input("Enter Product ID: "))
    if product is None:
        print("Product not found.")
        return

    print("Product Found")
    print("-" * 48)
    product.display_information()
    print("-" * 48)


# ---------------- Main program ----------------
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
            inventory.display_all()
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


if __name__ == "__main__":
    main()
