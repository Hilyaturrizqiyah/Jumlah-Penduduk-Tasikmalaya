import csv
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Tambahkan direktori utama proyek ke sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models import Penduduk  # Pastikan import model Anda sudah benar

# Ganti dengan string koneksi database MySQL Anda
DATABASE_URL = 'mysql+pymysql://dashboard_user:password@localhost/dashboard_db'  # Ganti dengan username dan password yang sesuai

# Buat engine dan session
engine = create_engine(DATABASE_URL, echo=True)  # Menambahkan echo=True untuk debugging
Session = sessionmaker(bind=engine)
session = Session()

def load_data_from_csv(csv_file_path):
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(f"Memasukkan data: {row}")  # Print data untuk verifikasi
            jenis_kelamin = row['jenis_kelamin'].strip().upper()
            tahun = int(row['tahun'])
            
            # Hanya proses data dari tahun terbaru, misal 2023
            if tahun != 2023:
                continue
            
            if jenis_kelamin not in ['LAKI-LAKI', 'PEREMPUAN']:
                continue  # Atau tangani dengan cara lain sesuai kebutuhan
            
            penduduk = Penduduk(
                kode_provinsi=int(row['kode_provinsi']),
                nama_provinsi=row['nama_provinsi'],
                kode_kabupaten_kota=int(row['kode_kabupaten_kota']),
                nama_kabupaten_kota=row['nama_kabupaten_kota'],
                kode_kecamatan=int(row['kode_kecamatan']),
                nama_kecamatan=row['nama_kecamatan'],
                kode_kelurahan=int(row['kode_kelurahan']),
                nama_kelurahan=row['nama_kelurahan'],
                jenis_kelamin=jenis_kelamin,
                jumlah_penduduk=int(row['jumlah_penduduk']),
                satuan=row['satuan'],
                tahun=tahun
            )
            session.add(penduduk)
            print(f"Data ditambahkan: {penduduk}")  # Print data yang ditambahkan
        session.commit()

# Ganti dengan path ke file CSV Anda
load_data_from_csv(r"C:\laragon\www\BIE-JDS\scripts\data.csv")
