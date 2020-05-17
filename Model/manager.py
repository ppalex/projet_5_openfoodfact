from Model.database import Database
from Model.product import ProductDownloader, ProductCleaner
from Model.api import Payload

import Configuration.config as config

config.load('./configuration/config.yml')


# Database MANAGER  #


class DatabaseManager(Database):
    def __init__(self):
        self.category_manager = CategoryManager()
        self.product_manager = ProductManager()
        self.store_manager = StoreManager()
        self.product_category_manager = ProductCategoryManager()
        self.product_store_manager = ProductStoreManager()

    def get_db(self):
        return self.db

    def cursor(self, dic=True):
        return self.db.cursor(dictionary=dic)

    def commit(self):
        self.db.commit()

    def close_cur(self):
        self.db.cursor.close()

    def close_conn(self):
        self.db.close()

    def create_tables(self):
        db = self.get_db()
        self.category_manager.create_category_table(db)
        self.product_manager.create_product_table(db)
        self.store_manager.create_store_table(db)
        self.product_category_manager.create_product_category_table(db)
        self.product_store_manager.create_product_store_table(db)

    def get_tables(self):
        db = self.get_db()
        cursor = db.cursor()
        sql = "SHOW TABLES"
        cursor.execute(sql)
        data = cursor.fetchall()

        return data

    def drop_tables(self):
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
        self.data = None

    def download_product(self, category_list):

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
        product_list = self.data
        return [category for product in product_list
                for category in product.categories]

    def get_all_stores(self):
        product_list = self.data

        return [store for product in product_list
                for store in product.stores]

# PRODUCT MANAGER #


class ProductManager():
    def __init__(self):
        pass

    def create_product_table(self, db):
        cursor = db.cursor()
        sql = "CREATE TABLE IF NOT EXISTS Product ( \
            id SMALLINT AUTO_INCREMENT PRIMARY KEY, \
            barcode VARCHAR(50) NOT NULL UNIQUE, \
            product_name VARCHAR(255) NOT NULL, \
            nutriscore_grade CHAR(1) NOT NULL, \
            product_description TEXT NOT NULL, \
            off_url VARCHAR(255) NOT NULL)"

        cursor.execute(sql)
        db.commit()
        cursor.close()

    def insert_product_db(product_list, db):
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
    def select_product_db(db, limit):
        cursor = db.cursor()

        sql = f"""SELECT product_name FROM product
                 ORDER BY RAND() LIMIT {limit}
                """

        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()

        return data

    @staticmethod
    def get_product_list_by_category_db(db_manager, limit, category_value):
        cursor = db_manager.get_db().cursor(dictionary=True)
        sql = f"""SELECT product_name, product.barcode FROM product
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
    def get_product_db(db_manager, barcode):
        cursor = db_manager.get_db().cursor(dictionary=True)
        sql = """SELECT product_id, barcode, product_name, nutriscore_grade,
                    GROUP_CONCAT(category_name SEPARATOR ',') AS categories
                    FROM product
                    INNER JOIN product_category
                    ON product.id = product_category.product_id
                        INNER JOIN category
                        ON category.id = product_category.category_id
                WHERE product.barcode = %s
                GROUP BY product_id
                """

        values = (barcode,)
        cursor.execute(sql, values)
        data = cursor.fetchone()
        cursor.close()
        return data

    @staticmethod
    def get_products_by_nutriscore_db(db_manager, nutriscrore, category):
        cursor = db_manager.get_db().cursor(dictionary=True)
        sql = """SELECT product_id, barcode, product_name, nutriscore_grade,
                    GROUP_CONCAT(category_name SEPARATOR ',') AS categories
                    FROM product
                    INNER JOIN product_category
                    ON product.id = product_category.product_id
                        INNER JOIN category
                        ON category.id = product_category.category_id
                    WHERE product.nutriscore_grade < %s
                    GROUP BY product_id
                    HAVING categories LIKE CONCAT('%', %s, '%')
                """

        values = (nutriscrore, category)
        cursor.execute(sql, values)
        data = cursor.fetchall()
        cursor.close()

        return data

    @staticmethod
    def get_product_by_store_db(db_manager, limit, category_value):
        cursor = db_manager.get_db().cursor(dictionary=True)
        sql = f"""SELECT product_name, product.barcode FROM product
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


# Catagory MANAGER #


class CategoryManager():
    def __init__(self):
        pass

    def create_category_table(self, db):
        cursor = db.cursor()
        sql = "CREATE TABLE IF NOT EXISTS Category ( \
                id SMALLINT AUTO_INCREMENT PRIMARY KEY, \
                category_name VARCHAR(255) NOT NULL UNIQUE)"
        cursor.execute(sql)
        db.commit()
        cursor.close()

    def insert_categories_db(category_list, db):
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
        cursor = db.cursor()
        sql = """CREATE TABLE IF NOT EXISTS Store (
                id SMALLINT AUTO_INCREMENT PRIMARY KEY,
                store_name VARCHAR(255) NOT NULL UNIQUE)
                """

        cursor.execute(sql)
        db.commit()
        cursor.close()

    def insert_store_db(store_list, db):
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
        cursor = db.cursor()

        sql = """CREATE TABLE IF NOT EXISTS Product_Category ( \
                product_id SMALLINT NOT NULL, \
                category_id SMALLINT NOT NULL, \
                CONSTRAINT pk_ProductStore PRIMARY KEY \
                (product_id, category_id))
                """

        cursor.execute(sql)
        db.commit()
        cursor.close()

    def insert_product_category_db(product_list, db):
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
        cursor = db.cursor()
        sql = """CREATE TABLE IF NOT EXISTS Product_Store ( \
                product_id SMALLINT NOT NULL, \
                store_id SMALLINT NOT NULL, \
                CONSTRAINT pk_ProductStore PRIMARY KEY (product_id, store_id))
                """
        cursor.execute(sql)
        db.commit()
        cursor.close()

    def insert_product_store_db(product_list, db):
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
        cursor = db.cursor()
        sql = """CREATE TABLE IF NOT EXISTS Product_Subsitute ( \
                product_id SMALLINT NOT NULL, \
                substitute_id SMALLINT NOT NULL, \
                    CONSTRAINT pk_ProductSubstitute \
                    PRIMARY KEY (product_id, substitute_id))
                """
        cursor.execute(sql)
        db.commit()
        cursor.close()

    def insert_product_substitute_db(product_id, substitute_id, db):
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
