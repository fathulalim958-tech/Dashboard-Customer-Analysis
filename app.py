import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point

orders_item_df = pd.read_csv("order_items_dataset.csv")
customer_df = pd.read_csv("customers_dataset.csv")

orders_item_df['shipping_limit_date'] = pd.to_datetime(orders_item_df['shipping_limit_date'])
orders_item_df['year'] = orders_item_df['shipping_limit_date'].dt.year
orders_item_df['month'] = orders_item_df['shipping_limit_date'].dt.month
orders_item_df['total_price'] = orders_item_df['price'] + orders_item_df['freight_value']


st.markdown("<h1 style='text-align: center;'>📊 Dashboard Customer Analysis <br> by Fathul Alim</h1>", unsafe_allow_html=True)
# ambil range tanggal
min_date = orders_item_df['shipping_limit_date'].min()
max_date = orders_item_df['shipping_limit_date'].max()

# date range picker
date_range = st.date_input(
    "Pilih Rentang Tanggal",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)
# filter berdasarkan tanggal
filtered_orders = orders_item_df[
    (orders_item_df['shipping_limit_date'] >= pd.to_datetime(date_range[0])) &
    (orders_item_df['shipping_limit_date'] <= pd.to_datetime(date_range[1]))
]
st.subheader("📆 Trend Revenue per Bulan (Interaktif)")
monthly_revenue = filtered_orders.groupby(
    filtered_orders['shipping_limit_date'].dt.month
)['total_price'].sum()
fig, ax = plt.subplots()
monthly_revenue.plot(kind='line', marker='o', ax=ax)
ax.set_title("Trend Revenue per Bulan")
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Revenue")
ax.set_xticks(monthly_revenue.index)
st.pyplot(fig)


st.subheader("📈 Trend Revenue per Tahun (Interaktif)")
yearly_revenue = filtered_orders.groupby(
    filtered_orders['shipping_limit_date'].dt.year
)['total_price'].sum()

fig2, ax2 = plt.subplots()
yearly_revenue.plot(kind='line', marker='o', ax=ax2)

ax2.set_title("Trend Revenue per Tahun")
ax2.set_xlabel("Tahun")
ax2.set_ylabel("Total Revenue")
ax2.set_xticks(yearly_revenue.index)
st.pyplot(fig2)

st.subheader("💡 Insight Lokasi")
st.write("Mayoritas customer terkonsentrasi pada wilayah tertentu (cluster terlihat jelas).")
st.write("Terdapat beberapa titik outlier yang kemungkinan merupakan data tidak valid.")


st.subheader("🌍 Distribusi Geolocation per State")
geo_state_summary = geolocations_df.groupby('geolocation_state').agg(
    total_point=('geolocation_zip_code_prefix', 'count'),
    unique_zip=('geolocation_zip_code_prefix', 'nunique')
).sort_values(by='total_point', ascending=False)
top_state = geo_state_summary.head(10)

st.subheader("🧠 Insight Otomatis")

total_customers = customer_df.shape[0]
top_city = customer_df['customer_city'].value_counts().idxmax()
top_state = customer_df['customer_state'].value_counts().idxmax()

st.write(f"Total Customer: **{total_customers}**")
st.write(f"Kota dengan customer terbanyak: **{top_city}**")
st.write(f"State dengan customer terbanyak: **{top_state}**")

st.subheader("🔍 Filter Data")

selected_state = st.selectbox(
    "Pilih State",
    options=customer_df['customer_state'].unique()
)

filtered_df = customer_df[customer_df['customer_state'] == selected_state]
st.write(f"Jumlah data pada state {selected_state}: {filtered_df.shape[0]}")
st.subheader("📊 Visualisasi")

# Top kota
city_counts = filtered_df['customer_city'].value_counts().head(10)

fig, ax = plt.subplots()
city_counts.plot(kind='bar', ax=ax)
ax.set_title("Top 10 Kota")
ax.set_xlabel("Kota")
ax.set_ylabel("Jumlah")
st.pyplot(fig)


st.subheader("🌍 Distribusi Customer per State")
state_counts = customer_df['customer_state'].value_counts()
st.bar_chart(state_counts)
