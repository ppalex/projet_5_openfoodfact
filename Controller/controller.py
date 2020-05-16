from Model.manager import DatabaseManager, ProductManager, \
                            CategoryManager, StoreManager


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