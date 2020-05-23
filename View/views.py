class View:
    def __init__(self, data):
        """Constructor of class View.

        Arguments:
            data {Dict} -- Dictionary that contains data to print.
        """
        self.data = data

    def print_menu(self):
        pass


class MainView(View):
    def __init__(self, data=None):
        """Constructor of class MainView

        Arguments:
            data {Dict} -- Dictionary that contains categories to print.
        """
        super().__init__(data)

    def print_menu(self):
        print("1 - Quel aliment souhaitez-vous remplacer ?")
        print("2 - Retrouver mes aliments substitués.")
        print("3 - Quitter.")

    @staticmethod
    def print_bye():
        """This method print the message before closing the app.
        """
        print("Merci et à bientôt")


class ViewCategory(View):
    def __init__(self, data):
        """Constructor of class ViewCategory

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


class ViewProduct(View):
    def __init__(self, data):
        """Constructor of the class ViewProduct.

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


class ViewSubstitute(View):
    def __init__(self, data):
        """Constructor of the class ViewSubstitute.

        Arguments:
            data {Dict} -- Dictionary that contains substitute to print.
        """
        super().__init__(data)

    def print_menu(self):
        """This method print the view for substitute.
        """
        print("""Substitut trouvé: \n ***************** \n""")
        print(self)
        print("Voulez-vous enregistrer le substitut dans vos favoris?")
        print("o/n")

    def substitut_not_found(self):
        print("""Nous n'avons pas trouvé de substitut avec un meilleur
        nutriscore dans la base.
        Veuillez alimenter la base avec plus de produit svp. \n""")

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


class ViewRecord(View):
    def __init__(self, data):
        """Constructor of the class ViewRecord.

        Arguments:
            data {Dict} -- Dictionary that contains substitute saved in
            database to print.
        """
        super().__init__(data)

    def print_menu(self):
        """This method print the view for records substitute.
        """
        if not self.data:
            print("""Aucun substitut enregistré pour le moment
                \n ***************** \n""")
        else:
            print(self)

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
