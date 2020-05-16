import abc
import requests


class DataDownloaderInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'load_data_source') and
                callable(subclass.load_data_source))


class Product:
    def __init__(self, **product_attributes):
        for attr_name, attr_value in product_attributes.items():
            if attr_name == 'categories':
                attr_value = attr_value.split(',')
            setattr(self, attr_name, attr_value)

    def __str__(self):
        string = ""
        attr = vars(self)
        for k, v in attr.items():
            string += f"{k} : {v} \n"
        return string

    @classmethod
    def create_product(cls, product_list):
        return [cls(**product) for product in product_list]


class ProductDownloader:
    def __init__(self, url, headers, payload):
        self.url = url
        self.headers = headers
        self.payload = payload

    def load_data_source(self):
        response = requests.request(
            "GET", self.url, headers=self.headers, params=self.payload)
        return response.json()


class ProductCleaner:
    def __init__(self):
        pass

    def create(products, category):

        product_list = [
            Product(**{
                'barcode': product.get('id', None),
                'product_name': product.get('product_name', None),
                'category': category,
                'nutriscore_grade': product.get('nutriscore_grade', None),
                'categories': product.get('categories', None).split(','),
                'stores': product.get('stores_tags', []),
                'description': product.get('ingredients_text_debug', None),
                'off_url': product.get('url', None)}
            ) for product in products['products']]

        return product_list

    def format_categories(product_list):
        for product in product_list:
            categories = []
            for category in product.categories:
                categories.append(category.lstrip().rstrip())
            setattr(product, 'categories', categories)
