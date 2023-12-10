import pandas as pd

customers_df = pd.read_csv("data/5784/noahs-customers.csv")
orders_df = pd.read_csv("data/5784/noahs-orders.csv")
items_df = pd.read_csv("data/5784/noahs-orders_items.csv")
products_df = pd.read_csv("data/5784/noahs-products.csv")

# get all pastries, assuming they are all with a SKU 'BKY'
#  pastries = products_df[products_df.sku.apply(lambda x : x.startswith("BKY"))]
#  pastries_skus = pastries.sku.to_list()


# get all orderids of pastries, assuming they are all with a SKU 'BKY'
pastries_items = items_df[items_df.sku.apply(lambda x: x.startswith("BKY"))]
pastries_orderids = pastries_items.orderid.to_list()

pastries_orders = orders_df[orders_df.orderid.apply(lambda x: x in pastries_orderids)]
# ordered before 5 am
pastries_orders.ordered = pd.to_datetime(pastries_orders.ordered)

# ordered before 2018 around dawn (around 4am)
pastries_orders = pastries_orders[
    pastries_orders.ordered.apply(lambda x: (3 < x.hour < 5 and x.year < 2020))
]

possible_customerids = pastries_orders.customerid.to_list()

possible_customers = customers_df[
    customers_df.customerid.apply(lambda x: x in possible_customerids)
]

# Only 2 women, one of which born in 1999, likely on tinder
#  1999-01-14    Renee Harmon  607-231-3605
print(possible_customers[["birthdate", "name", "phone"]])
