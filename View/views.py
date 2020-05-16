class View:
    def __init__(self, data):
        self.data = data

    def __str__(self):
        rpr = ""
        for k, v in self.data.items():
            rpr += f"{k} - {v} \n"

        return rpr
