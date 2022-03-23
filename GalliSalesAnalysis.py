#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 19:48:48 2022

@author: bigz-man
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

salesdf = pd.read_csv("/Users/bigz-man/Downloads/PythonYTProjects/GalliSalesAnalysis/Sales_Data/Sales_December_2019.csv")
salesdf.head()

all_sales = pd.DataFrame()

files = [file for file in os.listdir("/Users/bigz-man/Downloads/PythonYTProjects/GalliSalesAnalysis/Sales_Data")]

for file in files:
    salesdf = pd.read_csv("/Users/bigz-man/Downloads/PythonYTProjects/GalliSalesAnalysis/Sales_Data/"+file)
    all_sales = pd.concat([all_sales, salesdf])
    
all_sales.to_csv("all_sales.csv", index=False)

all_sales = pd.read_csv("all_sales.csv")

#%% Best Sales by Month

all_sales["Month"] = all_sales["Order Date"].str[0:2]
all_sales = all_sales.dropna(how = 'all')
all_sales = all_sales[all_sales['Order Date'].str[0:2] != 'Or']
all_sales["Month"] = all_sales["Month"].astype('int32')
all_sales["Quantity Ordered"] = pd.to_numeric(all_sales["Quantity Ordered"])
all_sales["Price Each"] = pd.to_numeric(all_sales["Price Each"])

all_sales["Sales"] = all_sales["Quantity Ordered"] * all_sales["Price Each"]
results = all_sales.groupby("Month").sum()

months = range(1,13)

plt.bar(months, results['Sales'])
plt.xticks(months)
plt.xlabel("Month Number")
plt.ylabel("Sales in USD ($)")
plt.show()

#%% Best Sales by City

def get_city(x):
    return x.split(',')[1].lstrip()

def get_state(x):
    return x.split(',')[2].split(' ')[1]

all_sales["City"] = all_sales["Purchase Address"].apply(lambda x: get_city(x) +
                                                        " (" + get_state(x) + ")")

city_sales = all_sales.groupby("City").sum()
city_sales_ordered = city_sales.sort_values(by = "Sales", ascending = False)
cities = [city for city, df in all_sales.groupby("City")]

plt.bar(cities, city_sales["Sales"])
plt.xticks(cities, rotation = 'vertical', size = 8)
plt.yticks(size = 8)
plt.xlabel("City")
plt.ylabel("Sales in USD ($)")

#%% Best Time to Advertise

all_sales["Order Date"] = pd.to_datetime(all_sales["Order Date"])
all_sales["Hour"] = all_sales["Order Date"].dt.hour
all_sales["Minute"] = all_sales["Order Date"].dt.minute

hours = [hour for hour, df in all_sales.groupby("Hour")]

plt.plot(hours, all_sales.groupby(["Hour"]).count())
plt.xticks(hours)
plt.grid()
plt.xlabel("Hours in a Day")
plt.ylabel("Number of Orders")

#%% Above but just in Atlanta

ATL_sales = all_sales.loc[all_sales["City"] == "Atlanta (GA)"] 

plt.plot(hours, ATL_sales.groupby(["Hour"]).count())
plt.xticks(hours)
plt.title("Atlanta")
plt.grid()
plt.xlabel("Hours in a Day")
plt.ylabel("Number of Orders")

#%% Most common items bought together

common = all_sales[all_sales["Order ID"].duplicated(keep = False)]
common["Grouped"] = common.groupby("Order ID")["Product"].transform(lambda x: ",".join(x))
common = common[["Order ID, Grouped"]].drop_duplicates()


#%% Most Bought Item

product_group = all_sales.groupby("Product")
most_common = product_group.sum()["Quantity Ordered"]

goods = [good for good, df in product_group]

plt.bar(goods, most_common)
plt.xticks(goods, rotation='vertical', size=8)
plt.ylabel("Sum of Product Sold")

