from .create_dummy_users import create_dummy_users
from .create_inventory import create_dummy_inventory
from .create_market import create_dummy_sales_and_purchases
from .create_pulls import create_random_pulls
from .create_trades import create_dummy_trades

def run():
    try:
        # create_dummy_users(50)
        # create_random_pulls(100)
        create_dummy_sales_and_purchases(50)
        # create_dummy_trades(50)
    except:
        print("An error occurred while populating the database.")
    