import pandas as pd

customers_df = pd.read_csv("data/5784/noahs-customers.csv")
orders_df = pd.read_csv("data/5784/noahs-orders.csv")
items_df = pd.read_csv("data/5784/noahs-orders_items.csv")
products_df = pd.read_csv("data/5784/noahs-products.csv")

# Get list of all cat food products
cat_food_skus: list = products_df[
    products_df.apply(lambda x: "Cat" in x.desc, axis=1)
].sku.to_list()

# Get a dict mapping for each orderid how many cat food items were ordered
orderid_to_cat_food_items: dict = (
    items_df.groupby("orderid")
    .apply(lambda x: sum(x.sku.apply(lambda y: y in cat_food_skus)))
    .to_dict()
)

# for each customerid get the number of catfood items ordered
customerids_to_cat_items_ordered: dict = (
    orders_df.groupby("customerid")
    .apply(lambda x: sum(x.orderid.apply(lambda y: orderid_to_cat_food_items[y])))
    .sort_values(ascending=False)
    .to_dict()
)

# filter by staten island customeres
possible_customers = customers_df[
    customers_df.citystatezip.apply(lambda x: x.startswith("Staten Island"))
]


# get the total amount of cat food ordered for each customer for all their orders
possible_customers["cat_items_ordered"] = possible_customers.customerid.apply(
    lambda x: customerids_to_cat_items_ordered.get(x, 0)
)


# Print top candidates, pick top lady
print(possible_customers.sort_values(by="cat_items_ordered", ascending=False).iloc[:3][
    ["phone", "name", "cat_items_ordered"]
])

# Solution:
# Nicole Wilson
# 631-507-6048
