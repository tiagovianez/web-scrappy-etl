import streamlit as st
import pandas as pd
import sqlite3

# Connect with database SQLite
conn = sqlite3.connect('../../data/quotes.db')

# Load data tables 'mercadolivre_itens' in a dataframe pandas
df = pd.read_sql_query("SELECT * FROM mercadolivre_itens", conn)

# Close connection with database
conn.close()

# Application title
st.title('Market Research - Casual Tennis on Mercado Livre')

# Application subtitle
st.subheader('KPIs system main')
col1, col2, col3 = st.columns(3)

# KPI 1: Total number itens
total_itens = df.shape[0]
col1.metric(label="Total number itens", value=total_itens)

# KPI 2: Number of Unique Tags
unique_brands = df['brand'].nunique()
col2.metric(label="Number of Unique Tags", value=unique_brands)

# KPI 3: New price medium
average_new_price = df['new_price'].mean()
col3.metric(label="New Average Price (R$)", value=f"{average_new_price:.2f}")

# Which brands are found most until the 10th page
st.subheader('brands are found most until the 10th page')
col1, col2 = st.columns([4, 2])
top_10_pages_brands = df.head(500)['brand'].value_counts().sort_values(ascending=False)
col1.bar_chart(top_10_pages_brands)
col2.write(top_10_pages_brands)

# Medium price by brand
st.subheader('Average price per brand')
col1, col2 = st.columns([4, 2])
average_price_by_brand = df.groupby('brand')['new_price'].mean().sort_values(ascending=False)
col1.bar_chart(average_price_by_brand)
col2.write(average_price_by_brand)

# What is the satisfaction by brand
st.subheader('satisfaction by brand')
col1, col2 = st.columns([4, 2])
df_non_zero_reviews = df[df['review_rating_number'] > 0]
satisfaction_by_brand = df_non_zero_reviews.groupby('brand')['review_rating_number'].mean().sort_values(ascending=False)
col1.bar_chart(satisfaction_by_brand)
col2.write(satisfaction_by_brand)