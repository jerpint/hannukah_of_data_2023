import pandas as pd

customers_df = pd.read_csv("data/5784/noahs-customers.csv")
orders_df = pd.read_csv("data/5784/noahs-orders.csv")
items_df = pd.read_csv("data/5784/noahs-orders_items.csv")
products_df = pd.read_csv("data/5784/noahs-products.csv")

# from 6.py we are looking for Sherri Long, let's get all her orders
sherri_customerid: int = customers_df[
    customers_df.name == "Sherri Long"
].customerid.iloc[0]

sherri_orders = orders_df[orders_df.customerid == sherri_customerid]
sherri_orderids: list[int] = sherri_orders.orderid.to_list()
#  sherri_items = items_df[items_df.orderid.apply(lambda x: x in sherri_orderids)]
sherri_items = items_df[items_df.orderid.isin(sherri_orderids)]

# Insight: coloured items all have a sku beginning with "COL"
# Find sherri orderids with colourd items ordered

sherri_items.groupby("orderid").apply(
    lambda x: "COL" in x.sku.apply(lambda y: y[:3]).unique()
)

sherri_color_orderids = sherri_items.groupby("orderid").apply(
    lambda x: "COL" in x.sku.apply(lambda y: y[:3]).unique()
)
sherri_color_orderids = sherri_color_orderids[sherri_color_orderids].index.to_list()

# Find all orderids before and after those of sherri (exclude her own)
candidate_orderids = [
    oid + x
    for oid in sherri_color_orderids
    for x in range(-2, 3)
    if oid + x not in sherri_orderids
]

# Find the orderids of those that are candidates and also bought a color item
refined_orderids = items_df[
    items_df.apply(lambda x: x.orderid in candidate_orderids and "COL" in x.sku, axis=1)
].orderid.to_list()

orders_df.ordered = pd.to_datetime(orders_df.ordered)  # convert to datetime

# Here, after printing, we can see that orderid 70502 is likely a good candidate as the order happened just a few
# seconds after sheeri's order

print(orders_df[orders_df.orderid.isin(refined_orderids)])
print(orders_df[orders_df.orderid.isin(sherri_color_orderids)])


# Let's print out the items of both orders:
skus = items_df[items_df.orderid.isin([70502, 70503])].sku.to_list()
print(products_df[products_df.sku.isin(skus)])

# We see they both ordered a Noah's poster
customerid = orders_df[orders_df.orderid == 70502].customerid.iloc[0]

print(customers_df[customers_df.customerid == customerid][["name", "phone"]])
# We find Carlos Myers 838-335-7157
