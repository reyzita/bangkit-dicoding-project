import streamlit as st
from streamlit.logger import get_logger
import numpy as np
import pandas as pd
import matplotlib as plt
import seaborn as sns
import requests
from io import StringIO

url = 'https://github.com/reyzita/dicoding-data-analysis-project/raw/96f046aa6003522df3ada08be5c7f6a1517b8ce9/pages/orders_df.csv'

# Membaca file CSV dari URL dan memuatnya ke dalam DataFrame orders_df
orders_df = pd.read_csv("orders_df.csv")
customers_df = pd.read_csv("customers_df.csv")
sellers_df = pd.read.csv("sellers_df.csv")

#Merge Order dan Customers dataset di orders_customer_df
orders_customers_df = pd.merge(
    left=orders_df,
    right=customers_df,
    how="left",
    left_on="customer_id",
    right_on="customer_id"
)

order_cust_status = orders_customers_df.groupby(by="order_status").order_id.nunique().sort_values(ascending=False)

#Membuat dataframe Sellers_city
sellers_city = sellers_df.groupby(by="seller_city").agg({
    "seller_id": "nunique"
})

#Membuat dataframe bystate_df
bystate_df = customers_df.groupby(by="customer_state").customer_id.nunique().reset_index()
bystate_df.rename(columns={
    "customer_id": "customer_count"
}, inplace=True)


### Streamlit Sidebar

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")


### Streamlit Main

st.header('Dicoding Collection Dashboard')
st.subheader('Dicoding Data Analysis First Project Dashboard - E-Commerce Public Dataset')
st.caption('Dataset: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce')

##1. Bagaimana performa order dari customer berdasarkan status ordernya?
st.subheader('Performance of Customer Orders Based on Their Order Status')
# Plot jumlah status order
fig, ax = plt.pyplot.subplots(figsize=(10, 6))
ax.bar(order_cust_status['Status'], order_cust_status['Number of the Status'])

# Menambahkan judul dan label sumbu
plt.title('Status Order Customer')
plt.xlabel('Status')
plt.ylabel('Number of the Status')

# Menampilkan nilai counts di dalam diagram batang
for i, value in enumerate(order_cust_status['Number of the Status']):
    plt.text(i, value + 5, str(value), ha='center', va='bottom')

# Menampilkan grafik di Streamlit
st.pyplot(fig)

st.caption('Question: How is the performance of customer orders based on their order status?')
st.caption('Conclusion: Based on the order status, there were 96478 orders with the status "Delivered", 1107 orders with the status "Shipped", 625 orders with the status "Canceled", 609 orders with the status "Unavailable", 314 orders with the status "Invoiced", 301 orders with the status "Processing", 5 orders with the status "Created", and 2 orders with the status "Approved". Therefore, it can be concluded that the performance of customer orders is running quite smoothly.')

##2. Bagaimana performa order "delivered" per tahun?
st.subheader('Number of Purchases per Year with Status "Delivered"')

orders_df['order_purchase_timestamp'] = pd.to_datetime(orders_df['order_purchase_timestamp'])
# Filter data berdasarkan order_status 'delivered'
delivered_orders = orders_df[orders_df['order_status'] == 'delivered']

# Mengelompokkan data berdasarkan tahun dan menghitung jumlah pembelian
purchase_per_year = delivered_orders.groupby(delivered_orders['order_purchase_timestamp'].dt.year)['order_id'].count()

# Tampilkan grafik menggunakan Streamlit

st.bar_chart(purchase_per_year)

# Menampilkan nilai counts di atas setiap batang
for i, value in enumerate(purchase_per_year):
    st.text(f"Year: {purchase_per_year.index[i]}, Purchases: {value}")

st.caption('Question: How is the performance of "delivered" orders per year?')
st.caption('Conclusion: Based on the bar chart, it can be observed that the status of "Delivered" orders shows an increasing trend with the number in the year 2016 being 267, in the year 2017 being 43428, and in the year 2018 being 52783 "Delivered" orders.')

##3. Bagaimana performa order "Delivered" pada tahun 2017?

# Filter data for the year 2017 and status 'delivered'
delivered_orders_2017 = orders_df[(orders_df['order_purchase_timestamp'].dt.year == 2017) & (orders_df['order_status'] == 'delivered')]

# Group data by month and count the number of purchases
purchase_per_month_2017 = delivered_orders_2017.groupby(delivered_orders_2017['order_purchase_timestamp'].dt.month)['order_id'].count()

# Plot the number of purchases per month
st.subheader('Number of Purchases with Status "Delivered" per Month in 2017')

# Create a bar chart
st.bar_chart(purchase_per_month_2017, use_container_width=True)

st.caption('Question: How is the performance of "Delivered" orders in 2017?')
st.caption('Conclusion: Based on the bar chart, it can be observed that the number of "Delivered" order statuses does not exhibit a trend as it fluctuates throughout certain months. The highest number of orders with the status "Delivered" occurs in the 11th month, which is November. Meanwhile, the lowest number of orders with the status "Delivered" occurs in the 1st month, which is January.')

##4.
st.subheader('Top 10 Cities with the Most Sellers?')
# Urutkan data berdasarkan jumlah penjual secara menurun
sellers_city_sorted = sellers_city.sort_values(by='seller_id', ascending=False)

# Ambil 10 kota dengan jumlah penjual terbanyak
top_10_cities = sellers_city_sorted.head(10)

# Buat plot batang
fig, ax = plt.pyplot.subplots(figsize=(10, 6))
ax.bar(top_10_cities.index, top_10_cities['seller_id'], color='red')

# Menambahkan nilai counts di dalam diagram batang
for i, value in enumerate(top_10_cities['seller_id']):
    plt.text(i, value + 5, str(value), ha='center', va='bottom')

# Menambahkan judul dan label sumbu
plt.title('Top 10 Cities with Most Sellers')
plt.xlabel('City')
plt.ylabel('Number of Sellers')

# Menampilkan grafik di Streamlit
st.pyplot(fig)
st.caption('Question: What are the top 10 cities with the most sellers?')
st.caption('Conclusion: Based on the bar chart, it is evident that the top 10 cities with the most sellers are Sao Paulo (694 sellers), Curitiba (127 sellers), Rio de Janeiro (96 sellers), Belo Horizonte (68 sellers), Ribeirao Preto (52 sellers), Guarulhos (50 sellers), Ibitinga (49 sellers), Santo Andre (45 sellers), Campinas (41 sellers), and Maringa (40 sellers).  Apart from these 10 cities, there is a need for more focused efforts to evenly distribute the number of sellers across different cities, thus enhancing the number of buyers in each city with available sellers.')

##5.
st.subheader('Customer Demographic Based on the State?')
plt.figure(figsize=(15, 10))
colors_ = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
ax = sns.barplot(
    x="customer_count",
    y="customer_state",
    data=bystate_df.sort_values(by="customer_count", ascending=False),
    palette=colors_
)
plt.title("Number of Customers by States", loc="center", fontsize=15)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='y', labelsize=12)

# Menambahkan nilai counts di dalam diagram batang
for i, v in enumerate(bystate_df.sort_values(by="customer_count", ascending=False)['customer_count']):
    ax.text(v + 5, i, str(v), color='black', va='center')

# Menampilkan grafik di Streamlit
st.pyplot(plt)

st.caption('Question: What is the customer demographic based on State?')
st.caption('Conclusion: According to the bar plot, the majority of customers are located in the state with the code SP, totaling 41476 customers, followed by the state with the code RJ, and then the state with the code MG with 46 customers.')

def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

