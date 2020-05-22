import random

from Model.product import Product, ProductCleaner


def list_to_dict(list):
    key = 1
    dic = {}
    for element in list:
        dic[key] = element
        key += 1
    return dic


def find_substitute(product_barcode, category_value, db_manager,
                    product_manager):
    """
    Arguments:
        product_barcode {String} -- Represents the barcode of the product.
        category_value {String} -- Represents the generic category value
                                    of the product.

    Returns:
        [Product] -- Represent a substitute to the product identified by
        the product barcode parameter.
    """
    product = product_manager.get_product_by_barcode_db(
        db_manager,
        product_barcode)

    product = Product(**product)
    ProductCleaner.split_string(product)
    nutriscore = product.nutriscore_grade

    product_list = product_manager.get_products_by_nutriscore_db(
        db_manager, nutriscore, category_value)

    product_list = Product.create_product(product_list)
    ProductCleaner().split_categories(product_list)

    substitute_list = filter(product_list, nutriscore)
    substitute = check_intersection(substitute_list, product)

    return substitute


def filter(product_list, n_ref):

    nutriscore_ref = ['a', 'b', 'c', 'd', 'e']
    substitute_list = []
    start_index = nutriscore_ref.index('a')
    end_index = nutriscore_ref.index(n_ref)

    while (start_index < end_index) and (not substitute_list):
        n = nutriscore_ref[start_index]
        for product in product_list:
            if product.nutriscore_grade == n:
                substitute_list.append(product)

        start_index += 1

    return substitute_list


def check_intersection(product_list, product_selected):
    best_product = []
    if len(product_list) > 0:
        best_product = random.choice(product_list)

        for product in product_list:
            intersection_product = list(
                set(product.categories).intersection(
                    product_selected.categories))

            intersection_best_product = list(
                set(best_product.categories).intersection(
                    product_selected.categories))

            if len(intersection_product) > len(intersection_best_product):
                best_product = product

    return best_product
