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
orders_df = pd.read_csv(url)


### Streamlit Sidebar

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")


### Streamlit Main

st.header('Dicoding Data Analysis First Project Dashboard - Reyzita Afrida')
st.subheader('E-Commerce Public Dataset')
st.caption('Dataset: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce')


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
