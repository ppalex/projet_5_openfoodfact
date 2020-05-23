import sys

import Configuration.config as config
import utils
from Model.manager import (CategoryManager, DatabaseManager, ProductManager,
                           ProductSubstituteManager, StoreManager)
from Model.product import Product
from View.views import (MainView, ViewCategory, ViewProduct, ViewRecord,
                        ViewSubstitute)

config.load('./configuration/config.yml')


class Controller:
    def __init__(self):
        """Constructor of the class Controller.
        The controller contains DatabaseManager object, ProductManager object
        CategoryManager object, StoreManager object,
        ProductSubstituteManager object
        """
        self.db_manager = DatabaseManager()
        self.product_manager = ProductManager()
        self.category_manager = CategoryManager()
        self.store_manager = StoreManager()
        self.product_substitute_manager = ProductSubstituteManager()

    def init(self):
        """ This method displays the main menu for the user and wait the input
        from user to continue.
        """
        value = ""
        main_view = MainView()

        while value not in ["1", "2", "3"]:
            main_view.print_menu()
            value = input()

        if value == "1":
            self.category_menu()

        elif value == "2":
            self.record_menu()

        elif value == "3":
            MainView.print_bye()
            sys.exit()

    def category_menu(self):
        """This method displays the category menu and wait the input
        from user to continue.
        """
        categories = config.value['CATEGORIES']
        categories = utils.list_to_dict(categories)

        view = ViewCategory(categories)

        expression = [str(x) for x in range(1, len(categories)+1)]
        value = ""
        ViewCategory.print_select()

        while value not in expression:
            view.print_menu()
            value = input()

        category = categories[int(value)]

        self.product_menu(category)

    def product_menu(self, category_value):
        """This method displays the product menu and wait the input
        from user to continue.
        """
        products = \
            self.product_manager.get_product_list_by_category_db(
                self.db_manager, 10, category_value)

        products = utils.list_to_dict(products)
        view = ViewProduct(products)

        value = ""
        expression = [str(x) for x in range(1, len(products)+1)]

        ViewProduct.print_select()

        while value not in expression:
            view.print_menu()
            value = input()

        product = Product(**products[int(value)])
        product_barcode = product.barcode

        if product.nutriscore_grade == 'a':
            ViewProduct.print_nutriscore_a()
            self.category_menu()
        else:
            substitute = utils.find_substitute(product_barcode, category_value,
                                               self.db_manager,
                                               self.product_manager)
            self.substitute_menu(substitute, product)

    def substitute_menu(self, substitute, product):
        """This method displays the substitute menu and wait the input
        from user to continue.
        """
        view = ViewSubstitute(substitute)
        value = ""

        if not substitute:
            view.substitut_not_found()
        else:
            view.print_menu()

            while value not in ["o", "n"]:
                value = input()

            if value == "o":
                product_id = product.id
                substitute_id = substitute.id
                db = self.db_manager.get_db()

                ProductSubstituteManager.insert_product_substitute_db(
                    product_id, substitute_id, db)

            elif value == "n":
                pass

        self.init()

    def record_menu(self):
        """This method displays the data stored by the user in db.
        It gets products and their substitutes.
        """
        product_list = ProductSubstituteManager.get_product_substitute(
            self.db_manager)
        view = ViewRecord(product_list)
        view.print_menu()

        self.init()
