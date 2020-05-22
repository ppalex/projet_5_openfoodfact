class View:
    def __init__(self, data):
        self.data = data

    def print_menu(self):
        pass


class View_Category(View):
    def __init__(self, data):
        super().__init__(data)

    @staticmethod
    def print_select():
        print("Sélectionnez la catégorie.")

    def print_menu(self):
        print(self)

    def __str__(self):
        rpr = ""
        for k, v in self.data.items():
            rpr += f"{k} - {v} \n"

        return rpr


class View_Product(View):
    def __init__(self, data):
        super().__init__(data)

    @staticmethod
    def print_select():
        print("Sélectionnez l'aliment.")

    @staticmethod
    def print_nutriscore_a():
        print("""L'aliment que vous avez sélectionné est déjà suffisamment sain
                  avec un nutriscore A \n""")

    def print_menu(self):
        print(self)

    def __str__(self):
        rpr = ""
        for k, v in self.data.items():
            rpr += f"{k} - {v['product_name']} - {v['nutriscore_grade']} \n"

        return rpr


class View_Substitute(View):
    def __init__(self, data):
        super().__init__(data)

    @staticmethod
    def print_bye():
        print("Merci et à bientôt")

    def print_menu(self):
        print("""Substitut trouvé: \n ***************** \n""")
        print(self)
        print("Voulez-vous enregistrer le substitut dans vos favoris?")
        print("o/n")

    def __str__(self):

        attr = vars(self.data)
        rpr = f"""
        Nom: {attr['product_name']} \n
        Description: {attr['product_description']} \n
        Nutriscore: {attr['nutriscore_grade']} \n
        URL: {attr['off_url']} \n
        Magasin: {attr['store_name']}
        """

        return rpr


class View_Record(View):
    def __init__(self, data):
        super().__init__(data)

    def __str__(self):
        rpr = ""

        for element in self.data:
            rpr += f"""
            Produit : {element['product']} ({element['barcode']})\n
            Substitut: {element['substitute']}\n
            Lien OFF: {element['off_url']}\n
                    """
            rpr += "*"*100
        return rpr
