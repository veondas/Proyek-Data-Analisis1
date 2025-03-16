# Bike Sharing Data Analysis & Dashboard

## Deskripsi Proyek
Proyek ini bertujuan untuk menganalisis dataset peminjaman sepeda (Bike Sharing Dataset) dan membuat dashboard menggunakan **Streamlit**. Dashboard ini untuk mengeksplorasi pola peminjaman sepeda berdasarkan berbagai variabel seperti cuaca dan musim

## Struktur Proyek
```
|-- Proyek Analysis Data/
|   |-- DataBaru.csv         # Dataset peminjaman sepeda
|   |-- main.py         # File utama untuk menjalankan dashboard Streamlit
|
|-- dataset/
|   |-- day.csv              # Dataset dari tabel day
|   |-- hour.csv             # Dataset dari tabel hour
|   |-- Readme.md            # Dokumentasi dataset
|
|-- Proyek_Analisis_Data1.ipynb           # Analisis eksploratif dalam Jupyter Notebook
|-- README.md                # Dokumentasi proyek
|-- requirements.txt         # Daftar library yang dibutuhkan
|-- url.txt                  # link streamlit
```

## Instalasi dan Menjalankan Program
### **1. Clone Repository**
Jalankan perintah berikut di terminal:
```bash
git clone https://github.com/veondas/Proyek-Data-Analisis1.git
cd Proyek-Analisis-Data1
```
### **2. Setup Environment - Anaconda**
```bash
conda create --name main-ds python=3.13.2
conda activate main-ds
pip install -r requirements.txt
```
### **3. Setup Environment - Shell/Terminal**
```bash
mkdir Proyek-Analisis-Data1
cd Proyek-Analisis-Data1
pipenv install
pipenv shell
pip install -r requirements.txt
```
### **4. Jalankan Dashboard Streamlit**
```bash
cd dashboard
streamlit run main.py
```
Dashboard akan terbuka di browser secara otomatis.

## Deployment
Dashboard dideploy menggunakan **Streamlit Community Cloud**.

### **Deploy dengan Streamlit Community Cloud**
1. **Upload proyek ke GitHub**.
2. **Buka** [Streamlit Community Cloud](https://share.streamlit.io/).
3. **copy and paste link repository GitHub**.
4. **Pilih file `dashboard/main.py` sebagai entry point**.
5. **Klik deploy**.

Setelah deployment berhasil, link dashboard dapat disalin dan dibagikan.
## Dataset
Dataset yang digunakan berasal dari Bike Sharing.

