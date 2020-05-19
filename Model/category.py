class Category:
    def __init__(self, category_name):
        """Constructor of the class Category.

        Arguments:
            category_name {String} -- Name of the category.
        """
        self.category_name = category_name

    def __str__(self):
        """This method return an object Category in String format
        """
        return f"{self.category_name}"
