class View:
    def __init__(self, data):
        self.data = data


class View_Category(View):
    def __init__(self, data):
        super().__init__(data)

    def __str__(self):
        rpr = ""
        for k, v in self.data.items():
            rpr += f"{k} - {v} \n"

        return rpr


class View_Product(View):
    def __init__(self, data):
        super().__init__(data)

    def __str__(self):
        rpr = ""
        for k, v in self.data.items():
            rpr += f"{k} - {v['product_name']} \n"

        return rpr
