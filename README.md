### DATA PENDUDUK TASIKMALAYA
## Deskripsi Proyek
Proyek ini bertujuan untuk menganalisis data penduduk di Tasikmalaya dengan menghasilkan beberapa insight berdasarkan data kecamatan, kelurahan, dan jenis kelamin. Dengan menyajikan informasi yang berguna dalam bentuk chart.

## Fitur
- **Analisis Demografi:**  
  Memahami distribusi penduduk berdasarkan kecamatan, kelurahan, dan jenis kelamin.

- **Visualisasi Data:**  
  Menyajikan data dalam bentuk chart yang mudah dipahami, seperti bar chart atau pie chart.

- **Insight Berdasarkan Data:**  
  Menyediakan insight dan interpretasi data yang membantu dalam pengambilan keputusan, seperti tren populasi dan perbandingan antara kecamatan.

## Data
Data yang digunakan dalam proyek ini mencakup:

- **Jumlah Penduduk per Kecamatan:**  
  Total penduduk yang tinggal di setiap kecamatan.

- **Jumlah Penduduk per Kelurahan:**  
  Total penduduk yang tinggal di setiap kelurahan.

- **Data Berdasarkan Jenis Kelamin:**  
  Proporsi pria dan wanita dalam populasi penduduk.

Sebelum memulai proyek ini, pastikan Anda memiliki perangkat lunak dan alat berikut:

- **[Python 3.8+](https://www.python.org/downloads/)**: Versi terbaru dari Python.
- **[pip](https://pip.pypa.io/en/stable/)**: Alat manajemen paket Python.
- **[Virtualenv](https://virtualenv.pypa.io/en/latest/)**: Untuk membuat lingkungan virtual Python (opsional, tapi disarankan).
- **[Node.js 18.x](https://nodejs.org/en/download/)**: Versi terbaru dari Node.js untuk mengelola dependensi JavaScript.
- **[MySQL 8.x](https://dev.mysql.com/downloads/mysql/)**: Untuk database aplikasi.

## Instalasi

Ikuti langkah-langkah berikut untuk menginstal dan menjalankan proyek ini:

1. **Clone Repositori**
```bash
https://github.com/Hilyaturrizqiyah/Jumlah-Penduduk-Tasikmalaya.git
```
2. **Buat Lingkungan Virtual dan Aktifkan (opsional)**

```bash
python -m venv venv
source venv/bin/activate  # Di Windows gunakan `venv\Scripts\activate`
```

3. **Instalasi Dependensi Python**

```bash
pip install -r requirements.txt
```

4. **Instalasi Dependensi JavaScript**

bash
Copy code
npm install

5. **Instalasi Dependensi PHP**

bash
Copy code
composer install

6. **Konfigurasi Environment**

Salin file .env.example ke .env dan sesuaikan konfigurasi database serta variabel lingkungan lainnya:

bash
Copy code
cp .env.example .env

7. **Migrasi Database**

Jalankan migrasi untuk membuat tabel-tabel yang dibutuhkan:

bash
Copy code
php artisan migrate
Menjalankan Aplikasi

Jalankan server lokal dengan perintah:

bash
Copy code
uvicorn app.main:app --reload
Akses aplikasi di http://localhost:8000.

Struktur Proyek
Berikut adalah struktur direktori proyek ini:
```
.
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── db.py
│   ├── models.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │       ├── __init__.py
│   │       └── penduduk.py
│   ├── static/
│       ├── js/
│       │   ├── d3.min.js
│       │   ├── penduduk_all.js
│       │   ├── penduduk_kecamatan.js
│       │   └── penduduk_kelurahan.js
│       ├── css/
│       │   ├── styles.css
│       └── index.html
├── requirements.txt
└── README.md
```
## Penggunaan
1. 