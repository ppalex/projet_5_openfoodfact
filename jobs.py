import Configuration.config as config

from Model.manager import DatabaseManager, ApiManager, ProductManager, \
                            CategoryManager, StoreManager, \
                            ProductCategoryManager, ProductStoreManager

config.load('./configuration/config.yml')


def initialize_job():

    category_list = config.value['CATEGORIES']

    db_manager = DatabaseManager()
    db_manager.create_tables()

    api_manager = ApiManager()
    api_manager.download_product(category_list)

    products = api_manager.data
    db = db_manager.get_db()

    categories = api_manager.get_all_categories()
    print("°"*20)
    print("INSERTION IN DB category: STARTED")
    CategoryManager.insert_categories_db(categories, db)
    print("INSERTION IN DB category: DONE")
    print("°"*20)
    print("INSERTION IN DB product: STARTED")
    ProductManager.insert_product_db(products, db)
    print("INSERTION IN DB product: DONE")
    print("°"*20)
    print("INSERTION IN DB product_category: STARTED")
    ProductCategoryManager.insert_product_category_db(products, db)
    print("INSERTION IN DB product_category: DONE")
    print("°"*20)
    all_stores = api_manager.get_all_stores()
    print("INSERTION IN DB store: STARTED")
    StoreManager.insert_store_db(all_stores, db)
    print("°"*20)
    print("INSERTION IN DB product_store: STARTED")
    ProductStoreManager.insert_product_store_db(products, db)

    db_manager.close_conn()


def drop_tables_job():
    db_manager = DatabaseManager()
    db_manager.drop_tables()
    db_manager.close_conn()
