import pandas as pd

customers_df = pd.read_csv("data/5784/noahs-customers.csv")
products_df = pd.read_csv("data/5784/noahs-products.csv")

# Cancer is born between June 22 and July 22
# Years of the rabbit: 2023, 2011, 1999, 1987, 1975, 1963, 1951, 1939, 1927
rabbit_years = [2023, 2011, 1999, 1987, 1975, 1963, 1951, 1939, 1927]
customers_df.birthdate = customers_df.birthdate.apply(pd.to_datetime)


def is_cancer(x: pd.DatetimeIndex):
    "Given a birthdate, figure out if it's a cancer birthdate or not"

    year = x.year
    day_min = pd.to_datetime(f"{year}-06-22")
    day_max = pd.to_datetime(f"{year}-07-22")
    return day_min < x < day_max


#  Filter out for both Cancer and rabbit years, still about 60 people
possible_customers = customers_df[
    customers_df.birthdate.apply(lambda x: x.year in rabbit_years)
]

possible_customers = possible_customers[possible_customers.birthdate.apply(is_cancer)]

# Find out which neighborhood the contractor lives in
contractor_phone = "332-274-4185"  # from 2.py
contractor_citystatezip = customers_df[
    customers_df.phone == contractor_phone
].citystatezip.iloc[0]

# Narrow it down to the same city
possible_customers = possible_customers[
    possible_customers.citystatezip == contractor_citystatezip
]

print(possible_customers.phone)
