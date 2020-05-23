import Configuration.config as config
from Model.api import Payload
from Model.database import Database
from Model.product import ProductCleaner, ProductDownloader

config.load('./configuration/config.yml')


# Database MANAGER  #


class DatabaseManager(Database):
    def __init__(self):
        """Constructor of the class DatabaseManager.
        """
        self.category_manager = CategoryManager()
        self.product_manager = ProductManager()
        self.store_manager = StoreManager()
        self.product_category_manager = ProductCategoryManager()
        self.product_store_manager = ProductStoreManager()
        self.product_substitute_manager = ProductSubstituteManager()

    def get_db(self):
        """This method return the db from instance.

        Returns:
            [Object] -- Instance of class DatabaseManager.
        """
        return self.db

    def cursor(self, dic=True):
        """This method return the cursor from the 'self' db object.

        Keyword Arguments:
            dic {bool} -- The return statement must be a dict (default: {True})

        Returns:
            [Cursor] -- Cursor for db.
        """
        return self.db.cursor(dictionary=dic)

    def commit(self):
        """This method commit data in db.
        """
        self.db.commit()

    def close_cur(self):
        """This method close the cursor connection.
        """
        self.db.cursor.close()

    def close_conn(self):
        """This method close the connection with db.
        """
        self.db.close()

    def create_tables(self):
        """This method creates all the tables in the DB.
        """
        db = self.get_db()
        self.category_manager.create_category_table(db)
        self.product_manager.create_product_table(db)
        self.store_manager.create_store_table(db)
        self.product_category_manager.create_product_category_table(db)
        self.product_store_manager.create_product_store_table(db)
        self.product_substitute_manager.create_product_substitute_table(db)

    def get_tables(self):
        """This method return the name of all tables from the db.

        Returns:
            [List] -- The list contains the name of the tables.
        """
        db = self.get_db()
        cursor = db.cursor()
        sql = "SHOW TABLES"
        cursor.execute(sql)
        data = cursor.fetchall()

        return data

    def drop_tables(self):
        """This method drop all the tables from the db.
        """
        db = self.get_db()
        cursor = db.cursor()
        table_list = self.get_tables()

        sql = "DROP TABLE IF EXISTS"
        values = ()

        for table in table_list:
            sql += " %s,"
            values += table
        sql = sql % values
        sql = sql[:-1]

        cursor.execute(sql)


# API MANAGER  #


class ApiManager:
    def __init__(self):
        """Constructor of the class ApiManager.
        """
        self.data = None

    def download_product(self, category_list):
        """This method download products by category from openfoodfact api.
             The data are recovered in self.data.

        Arguments:
            category_list {List} -- List of products categories.
        """
        url = config.value['API']['url']
        headers = {}
        data = []

        for category in category_list:
            payload = Payload(
                action=config.value['PAYLOAD']['action'],
                tag_0=category,
                tag_contains_0=config.value['PAYLOAD']['tag_contains_0'],
                tagtype_0=config.value['PAYLOAD']['tagtype_0'],
                page_size=config.value['PAYLOAD']['page_size'],
                json=config.value['PAYLOAD']['json'])

            product_downloader = ProductDownloader(
                url, headers, payload.get_payload_formatted())
            products_data = product_downloader.load_data_source()
            product_cleaner = ProductCleaner.create(
                products_data, category)
            ProductCleaner.format_categories(product_cleaner)
            data += product_cleaner

        self.data = data

    def get_all_categories(self):
        """This method get all categories from products recovered in self.data.

        Returns:
            [List] -- Contains all the possible categories from products.
        """
        product_list = self.data
        return [category for product in product_list
                for category in product.categories]

    def get_all_stores(self):
        """This method get all stores from products recovered in self.data.

        Returns:
            [List] -- Contains all the possible categories from products.
        """
        product_list = self.data

        return [store for product in product_list
                for store in product.stores]

# PRODUCT MANAGER #


class ProductManager():
    def __init__(self):
        """Constructor of the class ProductManager.
        """
        pass

    def create_product_table(self, db):
        """This method create the product table in the db.

        Arguments:
            db {Database} -- Database.
        """
        cursor = db.cursor()
        sql = """CREATE TABLE IF NOT EXISTS Product (
            id SMALLINT AUTO_INCREMENT PRIMARY KEY,
            barcode VARCHAR(50) NOT NULL UNIQUE,
            product_name VARCHAR(255) NOT NULL,
            nutriscore_grade CHAR(1) NOT NULL,
            product_description TEXT NOT NULL,
            off_url VARCHAR(255) NOT NULL)"""

        cursor.execute(sql)
        db.commit()
        cursor.close()

    def insert_product_db(product_list, db):
        """This method insert Products from list in table.

        Arguments:
            product_list {List} -- Contains Products objects.
            db {Database} -- Database.
        """
        cursor = db.cursor()

        for product in product_list:
            sql = """INSERT INTO Product (barcode,
                                            product_name,
                                            nutriscore_grade,
                                            product_description,
                                            off_url)
                        VALUES (%s, %s, %s, %s, %s)"""

            values = (product.barcode,
                      product.product_name,
                      product.nutriscore_grade,
                      product.description,
                      product.off_url)

            try:
                cursor.execute(sql, values)
            except Exception as e:
                print(e)

            db.commit()
        cursor.close()

    @staticmethod
    def get_product_by_name_db(db, limit):
        """This method get products from the db by product name.

        Arguments:
            db {Database} -- Database.
            limit {Int} -- Number of data to select.

        Returns:
            [Dict] -- Contains the data from the request.
        """
        cursor = db.cursor(dictionary=True)

        sql = f"""SELECT product_name FROM product
                 ORDER BY RAND() LIMIT {limit}
                """

        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()

        return data

    @staticmethod
    def get_product_list_by_category_db(db_manager, limit, category_value):
        """This method get products by category.

        Arguments:
            db {Database} -- Database.
            limit {Int} -- Limit of data to select.
            category_value {String} -- Food category.

        Returns:
            [Dict] -- Contains the data from the request.
        """
        cursor = db_manager.get_db().cursor(dictionary=True)
        sql = f"""SELECT product.id, product_name, product.barcode, product.nutriscore_grade
                    FROM product
                    INNER JOIN product_category
                    ON product.id = product_category.product_id
                        INNER JOIN category
                        ON category.id = product_category.category_id
                    WHERE category.category_name = %s
                    ORDER BY RAND() LIMIT {limit}
                    """
        values = (category_value,)
        cursor.execute(sql, values)
        data = cursor.fetchall()
        cursor.close()
        return data

    @staticmethod
    def get_product_by_barcode_db(db_manager, barcode):
        """This method get a product and his category by barcode.

        Arguments:
            db {Database} -- Database.
            barcode {String} -- Product barcode.

        Returns:
            Contains the data from the request.
        """
        cursor = db_manager.get_db().cursor(dictionary=True)
        sql = """SELECT product.id, barcode, product_name, nutriscore_grade,
                    GROUP_CONCAT(category_name SEPARATOR ',') AS categories
                    FROM product
                    INNER JOIN product_category
                    ON product.id = product_category.product_id
                        INNER JOIN category
                        ON category.id = product_category.category_id
                WHERE product.barcode = %s
                GROUP BY product.id
                """

        values = (barcode,)
        cursor.execute(sql, values)
        data = cursor.fetchone()
        cursor.close()
        return data

    @staticmethod
    def get_products_by_nutriscore_db(db_manager, nutriscrore, category):
        """This method get a list of product by nutriscore.

        Arguments:
            db {Database} -- Database.
            nutriscrore {String} -- Nutriscore of the product.
            category {String} -- Food category.

        Returns:
            [Dict] -- Contains the data from the request.
        """
        cursor = db_manager.get_db().cursor(dictionary=True)
        sql = """SELECT product.id, barcode, product_name, nutriscore_grade,
                            product_description, off_url, store_name,
                    GROUP_CONCAT(category_name SEPARATOR ',') AS categories
                    FROM product
                    INNER JOIN product_category
                    ON product.id = product_category.product_id
                        INNER JOIN category
                        ON category.id = product_category.category_id
                        INNER JOIN product_store
                            ON product.id = product_store.product_id
                                INNER JOIN store
                                ON store.id = store_id
                    WHERE product.nutriscore_grade < %s
                    GROUP BY product.id
                    HAVING categories LIKE CONCAT('%', %s, '%')
                """

        values = (nutriscrore, category)
        cursor.execute(sql, values)
        data = cursor.fetchall()
        cursor.close()

        return data

# Catagory MANAGER #


class CategoryManager():
    def __init__(self):
        """Constructor of the class CategoryManager.
        """
        pass

    def create_category_table(self, db):
        """This method create the category table in the db.

        Arguments:
            db {Database} -- Database.
        """
        cursor = db.cursor()
        sql = """CREATE TABLE IF NOT EXISTS Category (
                id SMALLINT AUTO_INCREMENT PRIMARY KEY,
                category_name VARCHAR(255) NOT NULL UNIQUE)"""
        cursor.execute(sql)
        db.commit()
        cursor.close()

    def insert_categories_db(category_list, db):
        """This method insert category from list in table.

        Arguments:
            product_list {List} -- Contains Products objects.
            db {Database} -- Database.
        """
        cursor = db.cursor()

        for category in category_list:
            sql = "INSERT IGNORE INTO Category (category_name) VALUES (%s)"
            values = category
            cursor.execute(sql, (values,))
            db.commit()
        cursor.close()

    @staticmethod
    def select_category_db(db, limit):
        cursor = db.cursor()

        sql = f"""SELECT category_name FROM category
                 ORDER BY RAND() LIMIT {limit}
                """

        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()

        return data

# Store MANAGER #


class StoreManager():
    def __init__(self):
        pass

    def create_store_table(self, db):
        """This method create the store table in the db.

        Arguments:
            db {Database} -- Database.
        """
        cursor = db.cursor()
        sql = """CREATE TABLE IF NOT EXISTS Store (
                id SMALLINT AUTO_INCREMENT PRIMARY KEY,
                store_name VARCHAR(255) NOT NULL UNIQUE)
                """

        cursor.execute(sql)
        db.commit()
        cursor.close()

    def insert_store_db(store_list, db):
        """This method insert store from list in table.

        Arguments:
            store_list {List} -- Contains store name.
            db {Database} -- Database.
        """
        cursor = db.cursor()

        for store in store_list:
            sql = "INSERT IGNORE INTO Store (store_name) VALUES (%s)"
            values = store
            cursor.execute(sql, (values,))
            db.commit()
        cursor.close()


# Product_Category MANAGER #


class ProductCategoryManager():

    def __init__(self):
        pass

    def create_product_category_table(self, db):
        """This method create the product_category table in the db.

        Arguments:
            db {Database} -- Database.
        """
        cursor = db.cursor()

        sql = """CREATE TABLE IF NOT EXISTS Product_Category (
                product_id SMALLINT NOT NULL,
                category_id SMALLINT NOT NULL,
                CONSTRAINT pk_ProductCategory
                PRIMARY KEY (product_id, category_id),
                FOREIGN KEY (product_id)
                    REFERENCES product (id),
                FOREIGN KEY (category_id)
                    REFERENCES category (id))
                """

        cursor.execute(sql)
        db.commit()
        cursor.close()

    def insert_product_category_db(product_list, db):
        """This method insert id product and category id from list in table.

        Arguments:
            product_list {List} -- Contains Products objects.
            db {Database} -- Database.
        """
        cursor = db.cursor()

        for product in product_list:
            for category in product.categories:
                sql = """INSERT INTO product_category (product_id, category_id)
                    SELECT DISTINCT product.id, category.id
                    FROM product, category
                    WHERE category.category_name = %s AND product.barcode = %s
                """

                values = (category, product.barcode)

                try:
                    cursor.execute(sql, values)
                except Exception as e:
                    print(e)
                db.commit()
        cursor.close()


# Product_Category MANAGER #


class ProductStoreManager():
    def __init__(self):
        pass

    def create_product_store_table(self, db):
        """This method create the product store table in the db.

        Arguments:
            db {Database} -- Database.
        """
        cursor = db.cursor()
        sql = """CREATE TABLE IF NOT EXISTS Product_Store (
                product_id SMALLINT NOT NULL,
                store_id SMALLINT NOT NULL,
                CONSTRAINT pk_ProductStore
                PRIMARY KEY (product_id, store_id),
                FOREIGN KEY (product_id)
                    REFERENCES product (id),
                FOREIGN KEY (store_id)
                    REFERENCES store (id))
                """
        cursor.execute(sql)
        db.commit()
        cursor.close()

    def insert_product_store_db(product_list, db):
        """This method insert product id and store id from list in table.

        Arguments:
            product_list {List} -- Contains Products objects.
            db {Database} -- Database.
        """
        cursor = db.cursor()

        for product in product_list:
            for store in product.stores:
                sql = """INSERT INTO product_store (product_id, store_id)
                    SELECT DISTINCT product.id, store.id
                    FROM product, store
                    WHERE store.store_name = %s AND product.barcode = %s
                """

                values = (store, product.barcode)

                try:
                    cursor.execute(sql, values)
                except Exception as e:
                    print(e)

                db.commit()

        cursor.close()


# Product_Substitute MANAGER #

class ProductSubstituteManager():
    def __init__(self):
        pass

    def create_product_substitute_table(self, db):
        """This method create the product_substitute table in the db.

        Arguments:
            db {Database} -- Database.
        """
        cursor = db.cursor()
        sql = """CREATE TABLE IF NOT EXISTS Product_Substitute (
                product_id SMALLINT NOT NULL,
                substitute_id SMALLINT NOT NULL,
                    CONSTRAINT pk_ProductSubstitute
                    PRIMARY KEY (product_id, substitute_id),
                FOREIGN KEY (product_id)
                    REFERENCES product (id),
                FOREIGN KEY (substitute_id)
                    REFERENCES product (id))
                """
        cursor.execute(sql)
        db.commit()
        cursor.close()

    def insert_product_substitute_db(product_id, substitute_id, db):
        """This method insert product id and product id (substitute) f
        table.

        Arguments:
            product_list {List} -- Contains Products objects.
            db {Database} -- Database.
        """
        cursor = db.cursor()

        sql = """INSERT INTO product_substitute (product_id, substitute_id)
            VALUES (%s, %s)
        """
        values = (product_id, substitute_id)

        try:
            cursor.execute(sql, values)
        except Exception as e:
            print(e)

        db.commit()
        cursor.close()

    @staticmethod
    def get_product_substitute(db_manager):

        cursor = db_manager.get_db().cursor(dictionary=True)
        sql = """SELECT  P.barcode, P.product_name AS "product",
                            S.product_name AS "substitute", S.off_url
                    FROM product P INNER JOIN
                    (product_substitute P_S INNER JOIN product S
                        ON P_S.substitute_id = S.id)
                    ON P.id = P_S.product_id
                """

        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()

        return data
