from abc import ABC, abstractmethod


class Product(ABC):

    def __init__(self, product_id, name, price, stock):
        product_id = str(product_id).strip()
        name = str(name).strip()

        if not product_id:
            raise ValueError("Product ID cannot be empty.")
        if not name:
            raise ValueError("Product name cannot be empty.")

        price = float(price)
        if price < 0:
            raise ValueError("Price cannot be negative.")

        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = 0
        self.update_stock(stock)

    @property
    def product_id(self):
        return self.__product_id

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @property
    def stock(self):
        return self.__stock

    def update_stock(self, quantity):
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Stock must be a non-negative whole number.")
        self.__stock = quantity

    def display_information(self):
        print(
            f"ID: {self.__product_id} | Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | Stock: {self.__stock}"
        )

    def to_dict(self):
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }

    @abstractmethod
    def get_fulfilment_info(self):
        pass