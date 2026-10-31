import json
from pathlib import Path

from can_be_shipped import CanBeShipped
from digital_product import DigitalProduct
from inventory import Inventory
from physical_product import PhysicalProduct

INVENTORY_FILE = Path(__file__).with_name("inventory.json")

PRODUCT_TYPES = {
    "physical": PhysicalProduct,
    "digital": DigitalProduct,
}


def create_product_from_dict(data):
    product_class = PRODUCT_TYPES.get(data.get("type"))
    if product_class is None:
        raise ValueError(f"unknown or missing product type: {data.get('type')!r}")
    return product_class.from_dict(data)


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
                inventory.add_product(create_product_from_dict(item))
            except (KeyError, TypeError, AttributeError, ValueError) as error:
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


def add_product(inventory):
    print("Add New Product")

    product_id = input("Product ID: ").strip()
    if not product_id:
        print("Product ID cannot be empty.")
        return

    if inventory.search_product(product_id) is not None:
        print("A product with that ID already exists.")
        return

    print("Product type:")
    print("1. Physical")
    print("2. Digital")
    product_type = input("Choose type: ").strip()

    if product_type not in ("1", "2"):
        print("Invalid product type.")
        return

    name = input("Product Name: ").strip()
    if not name:
        print("Product name cannot be empty.")
        return

    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))

        if product_type == "1":
            weight = float(input("Weight (kg): "))
            product = PhysicalProduct(product_id, name, price, stock, weight)
        else:
            download_size = float(input("Download size (MB): "))
            product = DigitalProduct(product_id, name, price, stock, download_size)
    except ValueError:
        print(
            "Enter non-negative numbers, with a whole-number stock quantity."
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
    print(product.get_fulfilment_info())

    if isinstance(product, CanBeShipped):
        print(f"Shipping cost: ${product.calculate_shipping_cost():.2f}")

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