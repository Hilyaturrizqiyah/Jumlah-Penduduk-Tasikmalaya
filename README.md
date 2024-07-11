### DATA PENDUDUK TASIKMALAYA
## Deskripsi Proyek
Proyek ini bertujuan untuk menganalisis data penduduk di Tasikmalaya dengan menghasilkan beberapa insight berdasarkan data kecamatan, kelurahan, dan jenis kelamin. Dengan menyajikan informasi yang berguna dalam bentuk chart.

## Fitur
Analisis Demografi: Memahami distribusi penduduk berdasarkan kecamatan, kelurahan, dan jenis kelamin.
Visualisasi Data: Menyajikan data dalam bentuk chart yang mudah dipahami.
Insight Berdasarkan Data: Menyediakan insight dan interpretasi data yang membantu pengambilan keputusan.
Data
Data yang digunakan dalam proyek ini mencakup:

## Jumlah Penduduk Tasikmalaya: Total jumlah penduduk.
Data Per Kecamatan: Jumlah penduduk per kecamatan.
Data Per Kelurahan: Jumlah penduduk per kelurahan.
Data Berdasarkan Jenis Kelamin: Jumlah penduduk berdasarkan jenis kelamin.

## Prasyarat
Sebelum memulai proyek ini, pastikan Anda memiliki perangkat lunak dan alat berikut:

## Instalasi
1. 

## Struktur Proyek
.
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── db.py
│   ├── models.py
│   ├── schemas.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── penduduk.py
│   │   │   └── user.py
│   │   ├── dependencies.py
│   │   └── exceptions.py
│   ├── static/
│   │   ├── js/
│   │   │   ├── d3.min.js
│   │   │   ├── penduduk_all.js
│   │   │   ├── penduduk_kecamatan.js
│   │   │   └── penduduk_kelurahan.js
│   │   ├── css/
│   │   │   ├── styles.css
│   │   └── index.html
│   └── templates/
│       ├── base.html
│       ├── penduduk_all.html
│       ├── penduduk_kecamatan.html
│       └── penduduk_kelurahan.html
│
├── tests/
│   ├── __init__.py
│   ├── test_routes.py
│   └── test_models.py
│
├── .env
├── requirements.txt
└── README.md

## Penggunaan
1. 