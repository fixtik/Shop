from shop_class import *
from custom_errors import *
import hashlib

class Shop:
    """
    Класс описания Интернет-магазина
    :param shop_name: название Интернет-магазина
    """

    DEFAULT_SHOP_NAME = 'default_shop'
    DEFAULT_USER_NAME = 'default_user'

    def __init__(self, shop_name: str = None):
        self.shop_name = shop_name

        # иные объекты
        self._user = []             # список пользователей магазина (объекты класса User)
        self._product_list = []     # список товаров в магазине (объекты класса Product)
        self._categories = []       # список категорий товаров и магазине (объекты класса Category)
        self._current_user = None         # текущий пользователь

    def __repr__(self):
        return f"{self.__class__.__name__}({self.shop_name})"

    @property
    def shop_name(self) -> str:
        return self._shop_name

    @shop_name.setter
    def shop_name(self, new_name: str):
        if isinstance(new_name, (str, int, float)):
            self._shop_name = str(new_name)
        else:
            self._shop_name = self.DEFAULT_SHOP_NAME
            print(f'Название магазина установлено как {self._shop_name}')

    @property
    def user(self) -> list[User]:
        """возращает список пользователей"""
        return self._user

    def add_user(self, new_user: User = None) -> None:
        """
        Добаление пользователя в интернет-магазин
        :param new_user: добавляемый пользователь
        """
        if new_user:
            Product._check_type(new_user, User)
        else:
            user_name = self._input_user_data('имя пользователя (логин)')
            user_pass = self._input_user_data('пароль')
            new_user = User(user_name, user_pass)
        self._user.append(new_user)

    def _input_user_data(self, print_string: str) -> str:
        """
        Ввод данных пользователя
        :return: введенная строка
        """
        return str(input(f"Введите {print_string}: "))

    def _search_user(self, user_name: str) -> [User, None]:
        """
        Поиск пользователя по его имени среди зарегистрированных
        :param user_name: искомое имя пользователя
        :return: объект User, если пользователь был зарегистрирован ранее, иначе None
        """
        for user in self._user:
            if user.login == user_name:
                return user
        return None

    def authentication(self) -> None:
        """Аутентификация пользователя в магазине"""
        user = self._search_user(self._input_user_data('имя пользователя (логин)'))
        if not user:
            raise invalid_user_name('пользователя с таким именем не существует')
        passwd = self._input_user_data(f'пароль пользователя {user.login}')
        if not hashlib.sha256(passwd.encode()).hexdigest() == user.password:
            raise invalid_password('введенный пароль неверен!')
        self._current_user = user

    @property
    def cur_user(self) -> User:
        return self._current_user

    @cur_user.setter
    def cur_user(self, user: User = None):
        """Установка текущего пользователя. Если пользователь не авторизован - берется пользователь по умолчанию"""
        if not user:
            self._current_user = User(self.DEFAULT_USER_NAME)
        else:
            Product._check_type(user, User)
            self._current_user = user

    def add_product(self, new_product: Product = None) -> None:
        """
        Добавляет товар в магазин
        :param new_product: объект Product или None
        """
        if new_product and isinstance(new_product, Product):
            self._product_list.append(new_product)
        else:
            name = self._input_user_data('название добавляемого товара')
            price = self._input_user_data('цену товара')
            rate = self._input_user_data('рейтинг товара')
            rate = float(rate) if rate.isdigit() else 1
            self._product_list.append(Product(name, price, rate))

    def add_products(self, *args) -> None:
        """Добавление нескольких товаров товаров"""
        for item in args:
            self.add_product(item)

    def print_product_list(self) -> str:
        """Возвращает "строку" с пепечнем товара в магазине"""
        result = ''
        for item in self._product_list:
            result += (f'\t{item}\n')
        return result


    def _add_category_to_list(self, new_cat: Category) -> None:
        """Добавление категории в список категорий"""
        Product._check_type(new_cat, Category)
        self._categories.append(new_cat)

    def _add_categories_to_list(self, *args: Category) -> None:
        """Добавление категорий в список"""
        for cat in args:
            self._add_category_to_list(cat)

    def create_new_category(self):
        """создание новой категории"""
        name = self._input_user_data('название категории')
        self._add_category_to_list(Category(name))

    def _seach_category_id_in_list(self, id: int) -> [Category, None]:
        """
        Поиск по категории по id
        :param id: искомый id
        :return: объект Category или None
        """
        Product._check_type(id, int)
        for cat in self._categories:
            if cat.id == id:
                return cat
        return None

    def _seach_category_name_in_list(self, name: str) -> [Category, None]:
        """
        Поиск по категории по названию
        :param name: искомое название
        :return: объект Category или None
        """
        Product._check_type(name, str)
        for cat in self._categories:
            if cat.name == name:
                return cat
        return None

    def add_products_to_category(self, *args, **kwargs) -> None:
        """Добавление продуктов в категорию"""
        for key in kwargs:
            if key == "id":
                cat = self._seach_category_id_in_list(kwargs[key])
            if key == "name":
                cat = self._seach_category_name_in_list(kwargs[key])
        for product in args:
            Product._check_type(product, Product)
            product.cat_id = cat.id
            cat.product_array = product

    def print_categorys_list(self) -> str:
        """Вывод списка категорий"""
        result = ''
        for cat in self._categories:
            result += f"\tid{cat.id} {cat.name}"
        return result

    def print_category_with_products(self) -> str:
        """Вывод списка товаров, разбитых по категориям"""
        result = ''
        for cat in self._categories:
            result += f'{cat.name}\n'
            for product in cat.product_array:
                result += f'\t{str(product)}\n'
        return result

    def add_to_cart(self, product: Product) -> None:
        if not self.cur_user:
            self.cur_user = None
        """Добавление товара в корзину текущего пользователя"""
        self.cur_user.basket.add_to_cart(product)

    def chek_order(self):
        total_cost = 0
        for item in self.cur_user.basket.order_array:
            total_cost += item.price
        print(f"К оплате {total_cost} у.е.")

if __name__ == '__main__':
    shop = Shop()               # создаем магазин

    print("Создание нового пользователя")
    shop.add_user()             # создаем пользователя
    print("Авторизация пользователя")
    shop.authentication()
    # добавление единичного товара
    shop.add_product(Product('Труселя', 100))

    # добавляем новую категорию
    shop._add_categories_to_list(Category('Нижнее белье'))

    # создаем новую категорию
    shop.create_new_category()

    # добавляем товары списком в категорию с id или с name
    shop.add_products_to_category(Product('Боксер', 150), Product('Боксер2', 150), Product('Боксер1', 150), Product('Боксер2', 150), id = 1)

    # вывод товаров с категориями
    print(shop.print_category_with_products())

    # добавляем товары в корзину
    shop.add_to_cart(Product('Боксер', 150))
    shop.add_to_cart(Product('Боксер_2', 150))

    # оформляем покупку через вывод общей суммы покупки
    shop.chek_order()


