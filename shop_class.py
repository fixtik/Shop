from typing import Any
import hashlib



class Product:
    """Класс для описания товара
        :param name: название товара
        :param price: цена за единицу товара
        :param rate: рейтинг товара
    """
    uid = 0

    def __init__(self, name: str, price: [int, float] = 1, rate: float = 1.0, cat_id: int = 0):
        self.name = name
        self.price = price
        self.rate = rate
        self.cat_id = cat_id

        self._uid = Product.uid = Product.uid + 1

    def __str__(self):
        return f"Товар: {self.name}, цена: {self.price}, рейтинг: {self.rate}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name},{self.price},{self.rate},{self.cat_id})"

    @staticmethod
    def _check_type(_object: Any, _type: type):
        if not isinstance(_object, _type):
            raise TypeError(f"Ожидается {_type}, получено {type(_object)}")

    @property
    def cat_id(self):
        return self._cat_id

    @cat_id.setter
    def cat_id(self, id: int):
        self._check_type(id, int)
        self._cat_id = id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._check_type(name, str)
        self._name = name

    @property
    def price(self) -> [int, float]:
        return self._price

    @price.setter
    def price(self, price: [int, float]) -> None:
        self._check_type(price, (int, float))
        self._price = price

    @property
    def rate(self) -> [int, float]:
        return self._rate

    @rate.setter
    def rate(self, rate: [int, float]) -> None:
        self._check_type(rate, (int, float))
        self._rate = rate


class Category:
    """
    Класс для описания категории товара
        :param name: название категории
        :param product_array: массив с товарами
    """
    next_id = 0

    def __init__(self, name: str, product_array: list[Product] = []):

        self._cat_id = Category.next_id = Category.next_id + 1
        self._product_array = []
        self.name = name
        self.product_array = product_array

    def __str__(self):
        items_string = '\t'
        for item in self.product_array:
            items_string += str(item) + '\n\t'
        return f"в категории {self.name} следующие товары: \n{items_string}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name},{self.product_array})"

    @property
    def id(self):
        return self._cat_id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        Product._check_type(name, str)
        self._name = name

    @property
    def product_array(self) -> list[Product]:
        return self._product_array

    @product_array.setter
    def product_array(self, *args: Product):
        """
        установка значений для товаров из категории
        :param product: объект типа Product или list[Product]
        """
        for item in args:
            if item:
                Product._check_type(item, Product)
                item.cat_id = self.id
                self._product_array.append(item)


class Basket:
    """
    Класс для описания корзины
    """

    def __init__(self, product: Product = None):
        self._order_array = []
        if product is not None:
            self.add_to_cart(product)

    def __str__(self):
        items_string = '\t'
        for item in self.order_array:
            items_string += str(item) + '\n\t'
        return f"в корзине следующие товары: \n{items_string}" if self.order_array else "корзина пуста"

    def __repr__(self):
        return f"{self.__class__.__name__}({self._order_array[0]})" if self._order_array else f"{self.__class__.__name__}(None)"

    @property
    def order_array(self) -> list[Product]:
        return self._order_array

    def add_to_cart(self, product: Product):
        """
        установка значений для товаров из категории
        :param product: объект типа Product или list[Product]
        """
        Product._check_type(product, Product)
        self._order_array.append(product)


class User:
    """
    Класс для описания покупателя
        :param login: Логин
        :param password: пароль
        :param user_basket: пользовательская корзина
    """
    DEFAULT_PASS = b'default_password'

    def __init__(self, login: str, password: Any = None, user_basket: Basket = None):
        self.login = login
        self.password = password
        self.basket = user_basket

    def __str__(self):
        return f"Пользователь {self.login}, {str(self.basket)}"

    def __repr__(self):
        pass_str = self.password if self.password else None
        basket_str = self.basket if self.basket else None
        return f"{self.__class__.__name__}({self.login}, {pass_str}, {basket_str})"

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, new_pass: Any = None) -> None:
        """
        Установка нового пароля поьзователя, пароль хранится в виде хэша
        :param new_pass: новое значение
        """
        if new_pass and isinstance(new_pass, (str, int, float)):
            self._password = hashlib.sha256(new_pass.encode()).hexdigest()
        else:
            print("Установлен пароль по умолчанию")
            self._password = hashlib.sha256(self.DEFAULT_PASS).hexdigest()

    @property
    def basket(self) -> Basket:
        return self._basket

    @basket.setter
    def basket(self, basket: Basket = None):
        if basket:
            self._basket = basket
        else:
            self._basket = Basket()


