from product import Product


class Inventory:
    """Manages a collection of Product objects (SRP)."""

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        """Add a Product. Returns False if the ID already exists."""
        if not isinstance(product, Product):
            raise TypeError("Only Product objects can be added.")
        if self.search_product(product.product_id) is not None:
            return False
        self.__products.append(product)
        return True

    def search_product(self, product_id):
        """Return the matching Product (case-insensitive) or None."""
        wanted = product_id.strip().casefold()
        for product in self.__products:
            if product.product_id.casefold() == wanted:
                return product
        return None

    def display_all(self):
        print("Current Inventory")
        print("-" * 48)

        if not self.__products:
            print("Inventory is empty.")

        for product in self.__products:
            product.display_information()

        print("-" * 48)

    def to_dict(self):
        """Inventory data in the same JSON structure as Week 5."""
        return {"products": [product.to_dict() for product in self.__products]}
