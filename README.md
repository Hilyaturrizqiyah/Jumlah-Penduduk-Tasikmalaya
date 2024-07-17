## DATA PENDUDUK TASIKMALAYA
### Deskripsi Proyek
Proyek ini bertujuan untuk menganalisis data penduduk di Tasikmalaya dengan menghasilkan beberapa insight berdasarkan data kecamatan, kelurahan, dan jenis kelamin. Dengan menyajikan informasi yang berguna dalam bentuk chart.

### Fitur
- **Analisis Demografi:**  
  Memahami distribusi penduduk berdasarkan kecamatan, kelurahan, dan jenis kelamin.

- **Visualisasi Data:**  
  Menyajikan data dalam bentuk chart yang mudah dipahami, seperti bar chart atau pie chart.

- **Insight Berdasarkan Data:**  
  Menyediakan insight dan interpretasi data yang membantu dalam pengambilan keputusan, seperti tren populasi dan perbandingan antara kecamatan.

### Data
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

### Instalasi

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

```bash
npm install
```

5. **Konfigurasi Database**

- Atur konfigurasi database di file `app/db.py` sesuai dengan pengaturan MySQL Anda.
- Buat database baru dan sesuaikan konfigurasi di `app/db.py`.

6. **Migrasi Database**

Jalankan migrasi untuk membuat tabel-tabel yang dibutuhkan:

```bash
python app/db.py
```

7. **Memuat Data ke Database**

Untuk memasukkan data ke dalam tabel `penduduk`, jalankan script `load_data.py`:

```bash
python app/scripts/load_data.py
```
Pastikan file `data.csv` berada di direktori `app/scripts/` dengan format yang sesuai.

### Menjalankan Aplikasi
Jalankan server lokal dengan perintah:

```bash
uvicorn app.main:app --reload
```
Akses aplikasi di http://localhost:8000.

### Struktur Proyek
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
│   │   ├── js/
│   │   │   ├── d3.min.js
│   │   │   ├── penduduk_all.js
│   │   │   ├── penduduk_kecamatan.js
│   │   │   └── penduduk_kelurahan.js
│   │   ├── css/
│   │   │   ├── styles.css
│   │   └── index.html
│   └── scripts/
│       ├── load_data.py
│       └── data.csv
├── requirements.txt
└── README.md

```
### Penggunaan
1. **Akses Aplikasi**
  Setelah menjalankan server lokal dengan perintah `uvicorn app.main:app --reload`, buka browser Anda. Kunjungi http://localhost:8000/penduduk/all untuk mengakses endpoint dan kunjungi http://127.0.0.1:8000/static/index.html untuk mengakses tampilan chart.

2. **Endpoint API**
  - `GET /all`
    **Deskripsi**
    Endpoint ini mengembalikan data keseluruhan penduduk berdasarkan kecamatan dan kelurahan, serta jumlah penduduk berdasarkan jenis kelamin.
    ```json
    {
      "data": {
          "Kecamatan1": {
              "kelurahan": {
                  "Kelurahan1": {
                      "laki_laki_per_kelurahan": 100,
                      "perempuan_per_kelurahan": 80,
                      "total_penduduk_per_kelurahan": 180
                  },
                  ...
              },
              "laki_laki_per_kecamatan": 500,
              "perempuan_per_kecamatan": 400,
              "total_penduduk_per_kecamatan": 900
          },
          ...
      },
      "total_laki_laki": 2000,
      "total_perempuan": 1800,
      "total_penduduk": 3800
    }
    ```

    **Cara Akses**
    Endpoint ini tidak memerlukan token.

  - `GET /kecamatan`
    **Deskripsi**
    Endpoint ini mengembalikan data jumlah penduduk berdasarkan jenis kelamin untuk kecamatan yang dipilih.

    **Query Parameters**
    `nama_kecamatan` (optional): Nama kecamatan yang ingin dilihat datanya. Jika tidak diberikan, data untuk semua kecamatan akan dikembalikan.

    ```json
    {
      "data": {
        "Kecamatan1": {
          "laki_laki": 500,
          "perempuan": 400,
          "total_penduduk": 900
        },
        ...
      }
    }
    ```
    **Cara Akses**
    Endpoint ini memerlukan token. Token harus disertakan dalam header HTTP dengan format `Authorization: Bearer <token>`, misalnya:
    ```http
      GET /kecamatan?nama_kecamatan=Kecamatan1
      Authorization: Bearer xYEq9m2f8C8X4F9fZvp2QbndsPfESunN
    ```

  - `GET /kelurahan`
    **Deskripsi**
    Endpoint ini mengembalikan data jumlah penduduk berdasarkan jenis kelamin untuk kelurahan yang dipilih.

    **Query Parameters**
    `nama_kelurahan`: Nama kelurahan yang ingin dilihat datanya.

    ```json
    {
      "data": {
        "Kelurahan1": {
            "kecamatan": "Kecamatan1",
            "laki_laki": 50,
            "perempuan": 60,
            "total_penduduk": 110
        }
      }
    }
    ```
    **Cara Akses**
    Endpoint ini memerlukan token. Token harus disertakan dalam header HTTP dengan format `Authorization: Bearer <token>`, misalnya:
    ```http
      GET /kelurahan?nama_kelurahan=Kelurahan1
      Authorization: Bearer xYEq9m2f8C8X4F9fZvp2QbndsPfESunN
    ```

  - `GET /kecamatan_list`
    **Deskripsi**
    Endpoint ini mengembalikan daftar nama kecamatan yang tersedia di database.

    **Query Parameters**
    `nama_kelurahan`: Nama kelurahan yang ingin dilihat datanya.

    ```json
    {
      "kecamatan": ["Kecamatan1", "Kecamatan2", ...]
    }
    ```
    **Cara Akses**
    Endpoint ini memerlukan token. Token harus disertakan dalam header HTTP dengan format `Authorization: Bearer <token>`, misalnya:
    ```http
      GET /kecamatan_list
      Authorization: Bearer xYEq9m2f8C8X4F9fZvp2QbndsPfESunN
    ```

  - `GET /kelurahan_list`
    **Deskripsi**
    Endpoint ini mengembalikan daftar nama kelurahan yang tersedia berdasarkan kecamatan yang dipilih.

    **Query Parameters**
    `kecamatan`: Nama kecamatan yang ingin dilihat daftar kelurahannya.

    ```json
    {
      "kecamatan": ["Kelurahan1", "Kelurahan2", ...]
    }
    ```
    **Cara Akses**
    Endpoint ini memerlukan token. Token harus disertakan dalam header HTTP dengan format `Authorization: Bearer <token>`, misalnya:
    ```http
      GET /kelurahan_list?kecamatan=Kecamatan1
      Authorization: Bearer xYEq9m2f8C8X4F9fZvp2QbndsPfESunN
    ```

3. **Interaksi dengan Data**
  - Gunakan dropdown untuk memilih kecamatan dan kelurahan yang ingin dianalisis.
  - Periksa visualisasi data yang disajikan dalam grafik bar dan pie chart untuk mendapatkan insight demografis.

  a. **Bagian Pie Chart**
    Menampilkan Pie Chart yang menunjukkan distribusi jumlah penduduk berdasarkan jenis kelamin. Data diambil dari endpoint `/all`.

  b. **Bagian Bar Chart Kecamatan**
  Menampilkan Bar Chart yang menunjukkan distribusi penduduk berdasarkan jenis kelamin untuk kecamatan yang dipilih. Data diambil dari endpoint `/kecamatan`.

  c. **Bagian Bar Chart Kelurahan**
  Menampilkan Bar Chart yang menunjukkan distribusi penduduk berdasarkan jenis kelamin untuk kelurahan yang dipilih setelah memilih kecamatan. Data diambil dari endpoint `/kelurahan`.

### Catatan
- `app/db.py`: Tempatkan konfigurasi database Anda di sini, ganti `mysql+pymysql://username:password@localhost/dbname` dengan konfigurasi MySQL Anda yang sesuai.

- `app/main.py`: Berfungsi untuk menjalankan aplikasi FastAPI. Sesuaikan jika diperlukan.

- `app/scripts/load_data.py`: Script untuk memuat data dari `data.csv` ke dalam tabel `penduduk`.

- `app/scripts/data.csv`: File CSV yang berisi data penduduk yang akan dimuat ke dalam database.

