import pandas as pd

customers_df = pd.read_csv("data/5784/noahs-customers.csv")
orders_df = pd.read_csv("data/5784/noahs-orders.csv")
items_df = pd.read_csv("data/5784/noahs-orders_items.csv")
products_df = pd.read_csv("data/5784/noahs-products.csv")


def get_initials(name: str):
    initials = []
    for n in name.split():
        initials.append(n[0])
    return "".join(initials)


# compute all initials
customers_df["initials"] = customers_df.name.apply(get_initials)

# find customer ids with JP initials
jp_customerids = customers_df[customers_df.initials == "JP"].customerid.to_list()

# find the orderids of those customers
jp_orderids = orders_df[
    orders_df.customerid.apply(lambda x: x in jp_customerids)
].orderid.to_list()

# get bagel SKUs
bagel_skus = products_df[
    products_df.apply(lambda x: "Bagel" in x.desc, axis=1)
].sku.to_list()

# Get all items that were bagels and ordered by someone with JP initials
##  filter by sku
filtered_items = items_df[items_df.sku.apply(lambda x: x in bagel_skus)]

##  filter by orderid of JP customers
filtered_items = filtered_items[
    filtered_items.orderid.apply(lambda x: x in jp_orderids)
]

# now get orderids of JP customers who ordered bagels
candidate_orderids = filtered_items.orderid.to_list()

# track it back to original orders
candidate_orders = orders_df[orders_df.orderid.apply(lambda x: x in candidate_orderids)]

# filter for orders that occured in 2017
valid_customerids = candidate_orders[
    candidate_orders.shipped.apply(lambda x: "2017" in x)
].customerid.to_list()

# Print the candidate phone numbers
print(
    customers_df[customers_df.customerid.apply(lambda x: x in valid_customerids)].phone
)
