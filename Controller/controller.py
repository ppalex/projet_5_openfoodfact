import Configuration.config as config
import utils
from Model.product import Product, ProductCleaner
from Model.manager import DatabaseManager, ProductManager, \
    CategoryManager, StoreManager, ProductSubstituteManager

from View.views import View_Category, View_Product, View_Substitute, \
                        View_Record


config.load('./configuration/config.yml')


class Controller:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.product_manager = ProductManager()
        self.category_manager = CategoryManager()
        self.store_manager = StoreManager()
        self.product_substitute_manager = ProductSubstituteManager()

    def init(self):

        value = ""

        while value not in ["1", "2"]:

            print("1 - Quel aliment souhaitez-vous remplacer ?")
            print("2 - Retrouver mes aliments substitués.")

            value = input()

        if value == "1":
            self.category_menu()

        elif value == "2":
            self.record_menu()

    def category_menu(self):
        categories = config.value['CATEGORIES']
        categories = utils.list_to_dict(categories)

        view = View_Category(categories)

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
            self.product_manager.get_product_list_by_category_db(
                self.db_manager, 10, category_value)

        products = utils.format_request(products)
        view = View_Product(products)
        value = ""
        expression = [str(x) for x in range(1, len(products)+1)]
        print("Sélectionnez l'aliment.")

        while value not in expression:
            print(view)
            value = input()

        product = Product(**products[int(value)])
        product_barcode = product.barcode

        substitute = self.find_substitute(product_barcode, category_value)

        self.substitute_menu(substitute, product)

    def substitute_menu(self, substitute, product):
        print("Substitut trouvé: \n")

        view = View_Substitute(substitute)
        value = ""
        print(view)
        print("Voulez-vous enregistrer le substitut dans vos favoris?")
        print("o/n")
        while value not in ["o", "n"]:
            value = input()

        if value == "o":
            product_id = product.id
            substitute_id = substitute.id
            db = self.db_manager.get_db()

            ProductSubstituteManager.insert_product_substitute_db(
                product_id, substitute_id, db)

        elif value == "n":
            print("Merci et à bientôt")

    def record_menu(self):

        product_list = ProductSubstituteManager.get_product_substitute(
            self.db_manager)
        view = View_Record(product_list)
        print(view)

    def find_substitute(self, product_barcode, category_value):

        product = self.product_manager.get_product_db(
            self.db_manager,
            product_barcode)

        product = Product(**product)
        ProductCleaner.split_string(product)
        nutriscore = product.nutriscore_grade

        product_list = self.product_manager.get_products_by_nutriscore_db(
            self.db_manager, nutriscore, category_value)

        product_list = Product.create_product(product_list)
        ProductCleaner().split_categories(product_list)

        substitute_list = utils.filter(product_list, nutriscore)
        substitute = utils.check_intersection(substitute_list, product)

        return substitute
