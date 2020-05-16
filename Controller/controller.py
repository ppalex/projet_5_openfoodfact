import Configuration.config as config
import utils

from Model.manager import DatabaseManager, ProductManager, \
    CategoryManager, StoreManager

from View.views import View


config.load('./configuration/config.yml')


class Controller:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.product_manager = ProductManager()
        self.category_manager = CategoryManager()
        self.store_manager = StoreManager()

    def init(self):

        value = ""

        while value not in ["1", "2"]:

            print("1 - Quel aliment souhaitez-vous remplacer ?")
            print("2 - Retrouver mes aliments substitués.")

            value = input()

        if value == "1":
            self.category_menu()

        elif value == "2":
            pass

    def category_menu(self):
        categories = config.value['CATEGORIES']       
        categories = utils.list_to_dict(categories)

        view = View(categories)

        expression = [str(x) for x in range(1, len(categories)+1)]
        value = ""
        print("Sélectionnez la catégorie.")

        while value not in expression:
            print(view)
            value = input()

        category = categories[int(value)]

        self.product_menu(category)

    def product_menu(self, category_value):
        products = \
            self.product_manager.get_product_by_category_db(
                self.db_manager, 10, category_value)

        products = utils.format_request(products)
        view = View(products)
        value = ""
        expression = [str(x) for x in range(1, len(products)+1)]
        print("Sélectionnez l'aliment.")

        while value not in expression:
            print(view)
            value = input()

        product = products[int(value)]
        product_barcode = product[1]

        self.find_product(product_barcode, category_value)
