import pandas as pd

customers_df = pd.read_csv("data/5784/noahs-customers.csv")
orders_df = pd.read_csv("data/5784/noahs-orders.csv")
items_df = pd.read_csv("data/5784/noahs-orders_items.csv")
products_df = pd.read_csv("data/5784/noahs-products.csv")

products_df.set_index("sku", inplace=True)

# Compute the margin for each item ordered
items_df["margin"] = items_df.apply(
    lambda x: x.unit_price - products_df.loc[x.sku].wholesale_cost, axis=1
)

# Compute the margin for each orderid
orderid_margins = items_df.groupby("orderid").apply(lambda x: sum(x.margin))

# Compute the margin for each customer
customerid_margins = orders_df.groupby("customerid").apply(
    lambda x: sum(x.orderid.apply(lambda y: orderid_margins.loc[y]))
)

# Sort the margins, get the worst of them all
worst_customerid: int = customerid_margins.sort_values().index[0]

# Print the name and phone number
print(customers_df[customers_df.customerid == worst_customerid][["phone", "name"]])
