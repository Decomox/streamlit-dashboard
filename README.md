# Proyek Dashboard Analisis Data

## Deskripsi Proyek

Proyek ini merupakan sebuah dashboard interaktif yang dibangun menggunakan bahasa pemrograman Python dan framework Streamlit. Dashboard ini memungkinkan pengguna untuk berinteraksi dengan data serta menampilkan visualisasi dan insight utama. Data utama diolah dan divisualisasikan secara dinamis melalui dashboard yang telah disiapkan.

## Struktur Proyek

Proyek ini terdiri dari beberapa folder dan file penting, yaitu:

- Folder `dashboard/` berisi file `dashboard.py` yang merupakan skrip utama untuk menjalankan dashboard menggunakan Streamlit.
- Folder `data/` berisi dua file, yaitu `day.csv` dan `hour.csv`, yang digunakan sebagai dataset tambahan untuk analisis lebih lanjut.
- File `notebook.ipynb` merupakan notebook Jupyter yang digunakan untuk eksplorasi data dan analisis awal.
- File `README.md` ini berfungsi sebagai dokumentasi proyek.
- File `requirements.txt` berisi daftar dependensi atau pustaka Python yang dibutuhkan untuk menjalankan proyek ini.
- File `url.txt` berisi tautan URL yang mengarah ke dashboard yang telah dideploy.

## Cara Instalasi

1. Clone repositori proyek ini ke komputer lokal Anda menggunakan perintah berikut:

   ```bash
   git clone https://github.com/Decomox/streamlit-dashboard.git
   ```
2. Masuk ke direktori proyek:

   ```
   cd streamlit-dashboard
   ```
3. Install semua dependensi yang diperlukan menggunakan file `requirements.txt`:

   ```
   pip install -r requirements.txt
   ```

## Cara Menjalankan

Menjalankan Dashboard Lokal

Untuk menjalankan dashboard Streamlit secara lokal, jalankan perintah berikut:

```
streamlit run dashboard.py
```

Anda juga bisa mengakses versi yang sudah dideploy melalui URL berikut:

[Dashboard yang sudah dideploy](https://app-dashboard-mtuc8jpwft8exmrrvvdhz8.streamlit.app/)

## Jupyter Notebook

File `notebook.ipynb` berisi eksplorasi data dan analisis awal. Buka file ini menggunakan Jupyter Notebook atau JupyterLab untuk melihat proses analisis yang telah dilakukan.

## Denpedensi

- `matplotlib`
- `pandas`
- `scipy`
- `seaborn`
- `statsmodels`
- `streamlit`
