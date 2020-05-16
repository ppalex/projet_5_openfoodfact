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