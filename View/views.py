class View:
    def __init__(self, data):
        """Constructor of class View.

        Arguments:
            data {Dict} -- Dictionary that contains data to print.
        """
        self.data = data

    def print_menu(self):
        pass


class View_Category(View):
    def __init__(self, data):
        """Constructor of class View_Category

        Arguments:
            data {Dict} -- Dictionary that contains categories to print.
        """
        super().__init__(data)

    @staticmethod
    def print_select():
        """This method print instruction for the user.
        """
        print("Sélectionnez la catégorie.")

    def print_menu(self):
        """This method print categories as a numbered list.
        """
        print(self)

    def __str__(self):
        """This method return the string representation of data.       

        Returns:
            [String] -- String as numbered list.
        """
        rpr = ""
        for k, v in self.data.items():
            rpr += f"{k} - {v} \n"

        return rpr


class View_Product(View):
    def __init__(self, data):
        """Constructor of the class View_Product.

        Arguments:
             data {Dict} -- Dictionary that contains products to print.
        """
        super().__init__(data)

    @staticmethod
    def print_select():
        """This method print instruction for the user.
        """
        print("Sélectionnez l'aliment.")

    @staticmethod
    def print_nutriscore_a():
        """This method print a message if the nutricore of a product is 'A'.
        """
        print("""L'aliment que vous avez sélectionné est déjà suffisamment sain
                  avec un nutriscore A \n""")

    def print_menu(self):
        """This method print the menu for products as a numbered list of product.
        """
        print(self)

    def __str__(self):
        rpr = ""
        for k, v in self.data.items():
            rpr += f"{k} - {v['product_name']} - {v['nutriscore_grade']} \n"
        return rpr


class View_Substitute(View):
    def __init__(self, data):
        """Constructor of the class View_Substitute.

        Arguments:
            data {Dict} -- Dictionary that contains substitute to print.
        """
        super().__init__(data)

    @staticmethod
    def print_bye():
        """This method print the message before closing the app.
        """
        print("Merci et à bientôt")

    def print_menu(self):
        """This method print the view for substitute.
        """
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
        """Constructor of the class View_Record.

        Arguments:
            data {Dict} -- Dictionary that contains substitute saved in 
            database to print.
        """
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
