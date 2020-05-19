class Store:
    def __init__(self, store_name):
        """Constructor of the class Store.

        Arguments:
            store_name {String} -- Name of the store.
        """
        self.store_name = store_name

    def __str__(self):
        return f"{self.store_name}"
