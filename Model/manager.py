from database import Database

import Configuration.config as config

config.load('./configuration/config.yml')


class DatabaseManager(Database):
    def __init__(self):
        super()


class ApiManager:
    def __init__(self):
        self.data = None

    def download_data_job(self, category_list):

        url = config.value['API']['url']
        headers = {}
        data = []

        for category in category_list:
            pass

        self.data = data

    def get_product(self):
        return self.data

    def get_all_categories(self):
        product_list = self.data
        return [category for product in product_list
                for category in product.categories]

    def get_all_stores(self):
        product_list = self.data

        return [store for product in product_list
                for store in product.stores]
        
        
