import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

#Reading Data
custom = pd.read_csv("data/olist_customers_dataset.csv")
loc = pd.read_csv("data/olist_geolocation_dataset.csv")
items = pd.read_csv("data/olist_order_items_dataset.csv")
payments = pd.read_csv("data/olist_order_payments_dataset.csv")
review = pd.read_csv("data/olist_order_reviews_dataset.csv")
order = pd.read_csv("data/coolist_orders_dataset.csv")
products = pd.read_csv("data/olist_products_dataset.csv")
sellers = pd.read_csv("data/olist_sellers_dataset.csv")
category = pd.read_csv("data/product_category_name_translation.csv")

#Merging into One dataset
merged_1 = pd.merge(items,payments,on = ["order_id"])
merge_2 = pd.merge(merged_1, review, on = ["order_id"])
merge_3 = pd.merge(merge_2, sellers, on = ["seller_id"])
merge_4 = pd.merge(merge_3, products, on = ["product_id"])
custom.rename(columns = {"customer_zip_code_prefix" : "zip_code_prefix"}, inplace = True)
loc.rename(columns = {"geolocation_zip_code_prefix" : "zip_code_prefix"}, inplace = True)
merge_5 = pd.merge(custom, loc, on = ["zip_code_prefix"])
merge_6 = pd.merge(merge_5, order, on = ["customer_id"])
merge_7 = pd.merge(merge_6, merge_4, on = ["order_id"])
merge_7.dropna(inplace = True)
merge_7.drop_duplicates(inplace=True)
merge_7.to_csv("revised_data.csv")