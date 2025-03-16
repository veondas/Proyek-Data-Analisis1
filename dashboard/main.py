import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from babel.numbers import format_currency
sns.set(style='dark')

# Streamlit Dashboard
st.title(':sparkles: Proyek Analisis Data: Bike Sharing :sparkles:')
st.write(
    """
    Nama        : Parveen Uzma Habidin  
    Email       : prvnuzmhbdn@gmail.com  
    ID Dicoding : MC325D5X1356
    """
)

# Load dataset
all_df = pd.read_csv("../dashboard/DataBaru.csv")

datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

# Visualisasi 1
st.subheader('Perbandingan Peminjaman Sepeda: Hari Libur vs Hari kerja')
 
# Layout with columns
col1, col2 = st.columns(2)

day_df = main_df.copy()
Totpmjmn = day_df.groupby('holiday')["cnt"].sum()
Thari = day_df["holiday"].value_counts()
Mean = Totpmjmn / Thari

data = pd.DataFrame({
    "Kategori": ["Hari Kerja", "Hari Libur"],
    "Rata-rata Peminjaman per Hari": Mean.values
})

with col1:
    total_peminjaman = day_df["cnt"].sum()
    st.metric("Total Peminjaman", value=total_peminjaman)

with col2:
    rata_rata_peminjaman = Mean.mean()
    st.metric("Rata-rata Peminjaman", value=rata_rata_peminjaman)

fig = px.bar(data, x="Kategori", y="Rata-rata Peminjaman per Hari", color="Kategori", title="Perbandingan Peminjaman Sepeda")
st.plotly_chart(fig)

#visualisasi 2
st.subheader("Rata-rata Peminjaman Sepeda Berdasarkan Musim")

# Mapping angka musim ke label
season_labels = ["Musim Semi", "Musim Panas", "Musim Gugur", "Musim Dingin"]

# Menghitung statistik peminjaman berdasarkan musim
stats = day_df.groupby("season")["cnt"].agg(total="sum", jmlhari="count", mean="mean").round(2)

# Membuat 2 kolom untuk menampilkan metrik
col1, col2 = st.columns(2)

with col1:
    total_peminjaman = stats["total"].sum()
    st.metric("Total Peminjaman", value=total_peminjaman)

with col2:
    rata_rata_peminjaman = stats["mean"].mean().round(2)
    st.metric("Rata-rata Peminjaman per Musim", value=rata_rata_peminjaman)

# Membuat bar chart untuk tren peminjaman berdasarkan musim
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(
    x=stats.index.astype(str),  # Menggunakan index sebagai label musim
    y=stats["mean"],  # Rata-rata peminjaman per musim
    ax=ax
)

# Styling
ax.set_xlabel("Musim", fontsize=15)
ax.set_ylabel("Rata-rata Peminjaman", fontsize=15)
ax.set_title("Tren Peminjaman Sepeda Berdasarkan Musim", fontsize=18)
ax.set_xticks(range(len(season_labels)))
ax.set_xticklabels(season_labels, rotation=30)
ax.grid(axis="y", linestyle="--", alpha=0.7)

# Menampilkan plot di Streamlit
st.pyplot(fig)

#Visualisasi 3
st.subheader("Pola Peminjaman Sepeda per Jam")

hr_df = pd.read_csv("../dataset/hour.csv")

# Grouping berdasarkan hari libur atau tidak
holiday_group = hr_df.groupby(['holiday', 'hr'])['cnt'].mean().reset_index()

# Menghitung total rata-rata peminjaman di hari libur dan hari biasa
mean_holiday = holiday_group[holiday_group["holiday"] == 1]["cnt"].mean().round(2)
mean_weekday = holiday_group[holiday_group["holiday"] == 0]["cnt"].mean().round(2)

# Membuat 2 kolom untuk menampilkan metrik
col1, col2 = st.columns(2)

with col1:
    st.metric("Rata-rata Per Jam (Hari Biasa)", value=mean_weekday)

with col2:
    st.metric("Rata-rata Per Jam (Hari Libur)", value=mean_holiday)

# Membuat plot scatter
fig, ax = plt.subplots(figsize=(12, 6))
scatter = sns.scatterplot(
    x='hr', y='cnt', hue='holiday', data=holiday_group,
    palette={0: 'blue', 1: 'red'}, alpha=0.7, ax=ax
)

# Styling plot
ax.set_xlabel('Jam dalam Sehari')
ax.set_ylabel('Rata-rata Peminjaman Sepeda')
ax.set_title('Pola Peminjaman Sepeda antara Hari Libur dan Hari Biasa')
ax.grid()

# Mengatur manual legend agar sesuai dengan warna
handles, _ = ax.get_legend_handles_labels()
ax.legend(handles, ["Hari Biasa", "Hari Libur"], title="Kategori")

# Menampilkan plot di Streamlit
st.pyplot(fig)

#Visualisasi 4
st.subheader("Clustering Berdasarkan Musim")
# Pilih fitur yang relevan (musim & jumlah peminjaman)
data = all_df[['season', 'cnt']]

# Normalisasi data
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

# Tentukan jumlah cluster optimal (misalnya 3)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
all_df['Cluster'] = kmeans.fit_predict(data_scaled)

# Mapping label cluster ke kategori peminjaman
cluster_labels = {0: "Peminjaman Rendah", 1: "Peminjaman Sedang", 2: "Peminjaman Tinggi"}
all_df['Cluster Label'] = all_df['Cluster'].map(cluster_labels)

# Membuat 2 kolom untuk menampilkan metrik
col1, col2 = st.columns(2)

with col1:
    total_low = all_df[all_df['Cluster Label'] == "Peminjaman Rendah"]['cnt'].sum()
    st.metric("Total Peminjaman Rendah", value=total_low)

with col2:
    total_high = all_df[all_df['Cluster Label'] == "Peminjaman Tinggi"]['cnt'].sum()
    st.metric("Total Peminjaman Tinggi", value=total_high)

# Membuat scatter plot
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(
    x=all_df['season'], 
    y=all_df['cnt'], 
    hue=all_df['Cluster Label'], 
    palette='spring', 
    ax=ax
)

# Styling plot
ax.set_xticks([1, 2, 3, 4])
ax.set_xticklabels(['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin'])
ax.set_xlabel('Musim')
ax.set_ylabel('Jumlah Peminjaman Sepeda')
ax.set_title('Clustering Peminjaman Sepeda Berdasarkan Musim')
ax.legend(title="Cluster")

# Menampilkan plot di Streamlit
st.pyplot(fig)