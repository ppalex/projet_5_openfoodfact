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
        dic[key] = element['product_name']
        key += 1
    return dic
