import pandas as pd
from tqdm import tqdm

tqdm.pandas()
customers_df = pd.read_csv("data/5784/noahs-customers.csv")
orders_df = pd.read_csv("data/5784/noahs-orders.csv")
items_df = pd.read_csv("data/5784/noahs-orders_items.csv")
products_df = pd.read_csv("data/5784/noahs-products.csv")

# Get the Series of all products that contain term "noah"
noah_products = products_df[products_df.desc.apply(lambda x: "noah" in x.lower())]

# For each customerid get their list of orderids
customerid_to_orderids = orders_df.groupby("customerid").apply(
    lambda x: x.orderid.to_list()
)

# For each customerid, use all their orderids to get all the purchased skus
customerid_to_skus = customerid_to_orderids.progress_apply(
    lambda x: items_df[items_df.orderid.isin(x)].sku.to_list()
)

# calculate the number of unique collector items each customer got
customerid_to_num_noah_items = customerid_to_skus.apply(
    lambda x: len(set(x).intersection(set(noah_products.sku.to_list())))
)

# Get the customerid of the one with max. items
customerid = customerid_to_num_noah_items.idxmax()

# get his info
print(customers_df[customers_df.customerid == customerid][["phone", "name"]])
