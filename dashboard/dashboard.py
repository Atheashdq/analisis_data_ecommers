import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import streamlit as st
import urllib
import numpy as np
from func import DataAnalyzer, BrazilMapPlotter


sns.set_theme(style='dark')

# Dataset
datetime_cols = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]
all_df = pd.read_csv("https://raw.githubusercontent.com/Atheashdq/analis-data/master/dashboard/df.csv")
all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(inplace=True)

# Geolocation Dataset
geolocation = pd.read_csv('https://raw.githubusercontent.com/Atheashdq/analis-data/master/dashboard/geolocation.csv')
data = geolocation.drop_duplicates(subset='customer_unique_id')

for col in datetime_cols:
    all_df[col] = pd.to_datetime(all_df[col])

min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()

# Sidebar
with st.sidebar:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(' ')
    with col2:
        st.image("https://raw.githubusercontent.com/Atheashdq/analis-data/master/dashboard/logo.JPG"
                 , width=100)
    with col3:
        st.write(' ')

    # Rentang Tanggal
    start_date, end_date = st.date_input(
        label="Pilih Rentang Tanggal",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

# Program Utama
main_df = all_df[(all_df["order_approved_at"] >= str(start_date)) & 
                 (all_df["order_approved_at"] <= str(end_date))]

function = DataAnalyzer(main_df)
map_plot = BrazilMapPlotter(data, plt, mpimg, urllib, st)

daily_orders_df = function.create_daily_orders_df()
sum_spend_df = function.create_sum_spend_df()
sum_order_items_df = function.create_sum_order_items_df()
review_score, common_score = function.review_score_df()
state, most_common_state = function.create_bystate_df()
order_status, common_status = function.create_order_status()

# Judul Dashboard
st.title("Dashboard Analisis Data E-Commerce X di Negara Brazil")

# Deskripsi
st.write("**Berikut merupakan Dashboard Analisis Data E-Commers X di Negara Brazil,**",
          "anda dapat melihat Total Pesanan Harian, Jumlah Belanja Pelanggan, Jenis Barang Belanjaan, Skor Ulasan, serta Data Demografi Pelanggan")


# Pesanan Harian yang Terkirim
st.subheader("Jumlah Pesanan Harian")
col1, col2 = st.columns(2)

with col1:
    total_order = daily_orders_df["order_count"].sum()
    st.markdown(f"Total Pesanan: **{total_order}**")

with col2:
    total_revenue = daily_orders_df["revenue"].sum()
    st.markdown(f"Total Pendapatan: **{total_revenue}**")

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(
    x=daily_orders_df["order_approved_at"],
    y=daily_orders_df["order_count"],
    marker="o",
    linewidth=2,
    color="#1e3aba"
)
ax.set_xlabel("Tanggal Persetujuan Pesanan", fontsize=12)
ax.set_ylabel("Total Pesanan", fontsize=12)
ax.tick_params(axis="x", rotation=45)
ax.tick_params(axis="y", labelsize=15)
st.pyplot(fig)

# Uang yang pelanggan belanjakan
st.subheader("Uang yang Dibelanjakan")
col1, col2 = st.columns(2)

with col1:
    total_spend = sum_spend_df["total_spend"].sum()
    st.markdown(f"Total belanja: **{total_spend}**")

with col2:
    avg_spend = sum_spend_df["total_spend"].mean()
    st.markdown(f"Rata-rata Belanja: **{avg_spend}**")

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(
    data=sum_spend_df,
    x="order_approved_at",
    y="total_spend",
    marker="o",
    linewidth=2,
    color="#c31f09"
)
ax.set_xlabel("Tanggal Persetujuan Pesanan", fontsize=12)
ax.set_ylabel("Total Belanja", fontsize=12)
ax.tick_params(axis="x", rotation=45)
ax.tick_params(axis="y", labelsize=15)
st.pyplot(fig)

# Order Items
st.subheader("Jenis Barang Belanjaan")
col1, col2 = st.columns(2)

with col1:
    total_items = sum_order_items_df["product_count"].sum()
    st.markdown(f"Total Barang: **{total_items}**")

with col2:
    avg_items = sum_order_items_df["product_count"].mean()
    st.markdown(f"Rata-rata Barang: **{avg_items}**")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(45, 25))

sns.barplot(x="product_count", y="product_category_name_english", hue='product_category_name_english', data=sum_order_items_df.head(5), palette="viridis", ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Jumlah Terjual", fontsize=80)
ax[0].set_title("Produk Paling Laris", loc="center", fontsize=90)
ax[0].tick_params(axis ='y', labelsize=55)
ax[0].tick_params(axis ='x', labelsize=50)

sns.barplot(x="product_count", y="product_category_name_english", hue='product_category_name_english', data=sum_order_items_df.sort_values(by="product_count", ascending=True).head(5), palette="viridis", ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Jumlah Terjual", fontsize=80)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Paling Sedikit Terjual", loc="center", fontsize=90)
ax[1].tick_params(axis='y', labelsize=55)
ax[1].tick_params(axis='x', labelsize=50)

st.pyplot(fig)

# Review Score
st.subheader("Skor Review")
col1,col2 = st.columns(2)

with col1:
    avg_review_score = review_score.mean()
    st.markdown(f"Rata-rata Skor Review: **{avg_review_score}**")

with col2:
    most_common_review_score = review_score.value_counts().index[0]
    st.markdown(f"Skor Review Terbanyak: **{most_common_review_score}**")

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=review_score.index, 
            y=review_score.values, 
            order=review_score.index,
            palette=["#068DA9" if score == common_score else "#D3D3D3" for score in review_score.index]
            )

plt.title("Ulasan Oleh Pelanggan Terhadap Layanan", fontsize=15)
plt.xlabel("Rating")
plt.ylabel("Jumlah")
plt.xticks(fontsize=12)

# Menambahkan label di atas setiap bar
for i, v in enumerate(review_score.values):
    ax.text(i, v + 5, str(v), ha='center', va='bottom', fontsize=12, color='black')

st.pyplot(fig)

# Customer Demographic
st.subheader("Demografi Pelanggan")
tab1, tab2 = st.tabs(["State", "Geolocation"])

with tab1:
    most_common_state = state.customer_state.value_counts().index[0]
    st.markdown(f"Lokasi Pelanggan Terbanyak: **{most_common_state}**")

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=state.customer_state.value_counts().index,
                y=state.customer_count.values,
                hue=state.customer_count.values,
                data=state,
                palette="viridis"
                    )
    plt.title("Jumlah Pelanggan Menurut Lokasi", fontsize=15)
    plt.xlabel("Lokasi")
    plt.ylabel("Jumlah Pelanggan")
    plt.xticks(fontsize=12)
    st.pyplot(fig)
    with st.expander("Lihat Penjelasan"):
        st.write("Kota São Paulo memiliki jumlah pelanggan terbanyak yaitu mencapai 40.000 pelanggan")
with tab2:
    brazil = mpimg.imread(urllib.request.urlopen('https://i.pinimg.com/originals/3a/0c/e1/3a0ce18b3c842748c255bc0aa445ad41.jpg'),'jpg')
    fig, ax = plt.subplots(figsize=(10,10))
    sns.scatterplot(data=data, x="geolocation_lng", y="geolocation_lat")
    plt.imshow(brazil, extent=[-73.98283055, -33.8,-33.75116944,5.4])
    plt.axis('off')
    st.pyplot(fig)


    with st.expander("Lihat Penjelasan"):
        st.write('pesanan yang terkirim merupakan 97,02 persen dari total dataset. Berdasarkan grafik yang ditampilkan, terdapat lebih banyak pelanggan di wilayah tenggara dan selatan pelanggan di kota-kota yang merupakan ibu kota (São Paulo, Rio de Janeiro, Porto Alegre, dan lainnya)')

st.caption('Atheash')
