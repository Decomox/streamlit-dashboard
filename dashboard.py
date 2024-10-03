import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm
import io

# Pengaturan halaman
st.set_page_config(page_title="Analisis Data - Bike Sharing", layout="wide")

# Fungsi untuk memuat data
@st.cache
def load_data():
    day_df = pd.read_csv('/data/day.csv')
    hour_df = pd.read_csv('/data/hour.csv')
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    return day_df, hour_df

day_df, hour_df = load_data()

# Sidebar navigasi
st.sidebar.title("Navigasi")
page = st.sidebar.selectbox(
    "Pilih Kategori",
    ["Home", "Tampilan Data", "Data Wrangling dan Informasi Dataset", "Exploratory Data Analysis", "Pertanyaan dan Konklusi"]
)

# HOME PAGE
if page == "Home":
    st.title("Proyek Analisis Data: Bike Sharing Dataset")
    st.markdown("**Nama:** Muhammad Syifa Ridhoni")
    st.markdown("**Email:** syifaridhoni04@gmail.com")

    st.header("Menentukan Pertanyaan Bisnis")
    st.markdown("""    
    1. Bagaimana pola penggunaan sepeda berdasarkan hari kerja dan hari libur?
    2. Bagaimana pengaruh kondisi cuaca (suhu, kelembaban, kecepatan angin) terhadap jumlah pengguna sepeda?
    """)

    st.header("Library yang Digunakan")
    st.markdown("""    
    - **Pandas**: Untuk manipulasi data
    - **Seaborn**: Untuk visualisasi data
    - **Matplotlib**: Untuk plot grafik
    - **Scipy**: Untuk analisis statistik
    - **Statsmodels**: Untuk regresi linier
    """)

# TAMPILAN DATA
elif page == "Tampilan Data":
    st.title("Tampilan Data CSV")

    st.subheader("Dataset Harian (day.csv)")
    st.write(day_df.head())

    st.subheader("Dataset Jam (hour.csv)")
    st.write(hour_df.head())

    st.subheader("Filter Data")
    filter_choice = st.selectbox("Pilih dataset yang ingin difilter", ["Harian", "Jam"])
    
    if filter_choice == "Harian":
        season = st.multiselect("Filter berdasarkan musim (1: musim dingin, 2: musim semi, 3: musim panas, 4: musim gugur)", day_df['season'].unique())
        if season:
            filtered_data = day_df[day_df['season'].isin(season)]
            st.write(filtered_data)
        else:
            st.write(day_df)
    else:
        hour = st.slider("Filter berdasarkan jam (0-23)", 0, 23, (0, 23))
        filtered_data = hour_df[(hour_df['hr'] >= hour[0]) & (hour_df['hr'] <= hour[1])]
        st.write(filtered_data)

# DATA WRANGLING DAN INFORMASI DATASET
elif page == "Data Wrangling dan Informasi Dataset":
    st.title("Data Wrangling dan Informasi Dataset")

    st.subheader("Informasi Dataset Harian")
    buffer = io.StringIO()  # Buat buffer untuk menangkap output
    day_df.info(buf=buffer)  # Tangkap output info() ke buffer
    s = buffer.getvalue()  # Ambil nilai dari buffer
    st.text(s)  # Tampilkan informasi ke Streamlit

    st.subheader("Informasi Dataset Jam")
    buffer = io.StringIO()  # Buat buffer untuk menangkap output
    hour_df.info(buf=buffer)  # Tangkap output info() ke buffer
    s = buffer.getvalue()  # Ambil nilai dari buffer
    st.text(s)  # Tampilkan informasi ke Streamlit

    st.subheader("Cleaning Data")
    st.markdown("Mengubah kolom tanggal menjadi tipe data datetime.")
    st.write(day_df[['dteday']].head())
    st.write(hour_df[['dteday']].head())

# EXPLORATORY DATA ANALYSIS
elif page == "Exploratory Data Analysis":
    st.title("Exploratory Data Analysis (EDA)")

    st.subheader("Distribusi Pengguna Sepeda")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(day_df['cnt'], kde=True, bins=30, ax=ax)
    ax.set_title("Distribution of Total Users")
    st.pyplot(fig)
    st.write("Grafik ini menunjukkan distribusi jumlah total pengguna sepeda.")

    st.subheader("Jumlah Pengguna Berdasarkan Tipe Hari")
    day_df['day_type'] = day_df.apply(lambda row: 'Holiday' if row['holiday'] == 1 else ('Working Day' if row['workingday'] == 1 else 'Weekend'), axis=1)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data=day_df, x='cnt', hue='day_type', kde=True, bins=30, ax=ax)
    ax.set_title('Distribution of Total Users by Day Type')
    st.pyplot(fig)
    st.write("Grafik ini menunjukkan jumlah pengguna sepeda berdasarkan tipe hari (hari kerja, akhir pekan, dan hari libur).")

    st.subheader("Korelasi Cuaca dan Penggunaan Sepeda")
    correlation = day_df[['temp', 'hum', 'windspeed', 'cnt']].corr()

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(correlation, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title("Correlation between Weather Conditions and Bike Usage")
    st.pyplot(fig)
    st.write("Heatmap ini menunjukkan korelasi antara kondisi cuaca (suhu, kelembaban, kecepatan angin) dan penggunaan sepeda.")

# Pertanyaan & Konklusi
elif page == "Pertanyaan dan Konklusi":
    st.title("Pertanyaan dan Konklusi")
    
    st.subheader("Pertanyaan 1: Pola Penggunaan Sepeda Berdasarkan Hari Kerja dan Hari Libur")
    
    # Pastikan kolom 'day_type' ada di dataset
    if 'day_type' not in day_df.columns:
        day_df['day_type'] = day_df.apply(lambda row: 'Holiday' if row['holiday'] == 1 else ('Working Day' if row['workingday'] == 1 else 'Weekend'), axis=1)
    
    # Periksa apakah kolom yang dibutuhkan ada
    if 'dteday' in day_df.columns and 'cnt' in day_df.columns and 'day_type' in day_df.columns:
        # Cek apakah ada nilai NaN di kolom yang digunakan
        if day_df[['dteday', 'cnt', 'day_type']].isnull().values.any():
            st.error("Terdapat nilai NaN pada kolom yang digunakan untuk plot. Harap bersihkan data.")
        else:
            # Line plot penggunaan sepeda harian
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.lineplot(x='dteday', y='cnt', hue='day_type', data=day_df, ax=ax)
            ax.set_title('Trend Penggunaan Sepeda Harian Berdasarkan Tipe Hari')
            ax.tick_params(axis='x', rotation=45)
            st.pyplot(fig)
    else:
        st.error("Kolom yang dibutuhkan untuk plot tidak ditemukan dalam dataset.")
    
    # T-test antara hari kerja dan hari libur
    st.subheader("Uji T-Test Pengguna Sepeda Hari Kerja vs Libur")
    working_day_users = day_df[day_df['workingday'] == 1]['cnt']
    weekend_users = day_df[day_df['workingday'] == 0]['cnt']
    
    if len(working_day_users) > 0 and len(weekend_users) > 0:
        t_stat, p_value = stats.ttest_ind(working_day_users, weekend_users)
        st.write(f"T-statistic: {t_stat:.2f}, P-value: {p_value:.4f}")
        
        if p_value < 0.05:
            st.write("Ada perbedaan signifikan antara penggunaan sepeda pada hari kerja dan akhir pekan/libur.")
        else:
            st.write("Tidak ada perbedaan signifikan antara penggunaan sepeda pada hari kerja dan akhir pekan/libur.")
    else:
        st.error("Data tidak cukup untuk melakukan uji t-test.")
    
    st.subheader("Pertanyaan 2: Pengaruh Kondisi Cuaca terhadap Penggunaan Sepeda")
    
    # Regresi Linier
    if 'temp' in day_df.columns and 'hum' in day_df.columns and 'windspeed' in day_df.columns:
        X = day_df[['temp', 'hum', 'windspeed']]
        y = day_df['cnt']
        X = sm.add_constant(X)
        model = sm.OLS(y, X).fit()
        st.write(model.summary())
        
        # Scatter plot dengan garis regresi
        st.subheader("Pengaruh Suhu terhadap Penggunaan Sepeda")
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.regplot(x='temp', y='cnt', data=day_df, line_kws={'color':'red'}, ax=ax)
        ax.set_title('Pengaruh Suhu terhadap Jumlah Pengguna Sepeda')
        st.pyplot(fig)
        st.write("Grafik ini menunjukkan hubungan antara suhu dan jumlah pengguna sepeda.")
        
        st.subheader("Pengaruh Kelembaban terhadap Penggunaan Sepeda")
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.regplot(x='hum', y='cnt', data=day_df, line_kws={'color':'red'}, ax=ax)
        ax.set_title('Pengaruh Kelembaban terhadap Jumlah Pengguna Sepeda')
        st.pyplot(fig)
        st.write("Grafik ini menunjukkan hubungan antara kelembaban dan jumlah pengguna sepeda.")
        
        st.subheader("Pengaruh Kecepatan Angin terhadap Penggunaan Sepeda")
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.regplot(x='windspeed', y='cnt', data=day_df, line_kws={'color':'red'}, ax=ax)
        ax.set_title('Pengaruh Kecepatan Angin terhadap Jumlah Pengguna Sepeda')
        st.pyplot(fig)
        st.write("Grafik ini menunjukkan hubungan antara kecepatan angin dan jumlah pengguna sepeda.")
    else:
        st.error("Kolom yang dibutuhkan untuk regresi tidak ditemukan dalam dataset.")

    st.subheader("Konklusi Pertanyaan 1")

    st.write("Analisis menunjukkan bahwa pola penggunaan sepeda antara hari kerja dan hari libur tidak memiliki perbedaan yang signifikan. Dari hasil uji t-test, T-statistic sebesar 1.654 menunjukkan bahwa ada perbedaan kecil antara jumlah pengguna sepeda pada hari kerja dan akhir pekan/hari libur, namun nilai ini tidak cukup besar untuk dianggap signifikan. P-value yang dihasilkan sebesar 0.098 menunjukkan probabilitas bahwa perbedaan ini terjadi secara kebetulan, jika tidak ada perbedaan nyata antara kedua kelompok. Karena P-value ini lebih besar dari threshold 0.05, hasilnya tidak dianggap signifikan secara statistik pada tingkat kepercayaan 95%. Dengan demikian, meskipun ada fluktuasi dalam penggunaan sepeda, tidak ada bukti yang cukup kuat untuk menyatakan bahwa hari kerja dan hari libur mempengaruhi jumlah pengguna sepeda secara signifikan.")

    st.subheader("Konklusi Pertanyaan 2")

    st.write("Hasil analisis regresi linier menunjukkan bahwa suhu memiliki pengaruh positif yang signifikan terhadap jumlah pengguna sepeda, di mana setiap kenaikan satu derajat Celsius dalam suhu dapat meningkatkan jumlah pengguna sekitar 6625.53 orang. Di sisi lain, kelembaban dan kecepatan angin memiliki pengaruh negatif yang signifikan terhadap penggunaan sepeda. Kenaikan kelembaban sebesar satu persen diperkirakan mengurangi jumlah pengguna sebanyak 3100.12 orang, sementara setiap peningkatan satu unit kecepatan angin dapat mengurangi jumlah pengguna sepeda sebesar 4806.93 orang. Oleh karena itu, kondisi cuaca berperan penting dalam mempengaruhi pola penggunaan sepeda, dan dapat menjadi dasar bagi pengambil kebijakan dalam merancang program-program promosi yang lebih efektif untuk meningkatkan penggunaan sepeda dalam kondisi cuaca tertentu.")
