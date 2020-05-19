def list_to_dict(list):
    key = 1
    dic = {}
    for element in list:
        dic[key] = element
        key += 1
    return dic


def format_request(dic_data):
    key = 1
    dic = {}
    for element in dic_data:
        dic[key] = element
        key += 1
    return dic


def filter(product_list, n_ref):

    nutriscore_ref = ['a', 'b', 'c', 'd', 'e']
    subsitute_list = []
    start_index = nutriscore_ref.index('a')
    end_index = nutriscore_ref.index(n_ref)

    while (start_index < end_index) and (not subsitute_list):
        n = nutriscore_ref[start_index]
        for product in product_list:
            if product.nutriscore_grade == n:
                subsitute_list.append(product)

        start_index += 1

    return subsitute_list


def check_intersection(product_list, product_selected):
    
    best_product = product_list[0]

    for product in product_list:
        intersection_product = list(
            set(product.categories).intersection(product_selected.categories))
        intersection_best_product = list(
            set(best_product.categories).intersection(
                product_selected.categories))

        if len(intersection_product) > len(intersection_best_product):
            best_product = product

    return best_product
