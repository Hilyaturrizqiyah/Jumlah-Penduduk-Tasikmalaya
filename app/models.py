from sqlalchemy import Column, Integer, String
from .db import Base

class Penduduk(Base):
    __tablename__ = "penduduk"
    id = Column(Integer, primary_key=True, index=True)
    kode_provinsi = Column(Integer)
    nama_provinsi = Column(String)
    kode_kabupaten_kota = Column(Integer)
    nama_kabupaten_kota = Column(String)
    kode_kecamatan = Column(Integer)
    nama_kecamatan = Column(String)
    kode_kelurahan = Column(Integer)
    nama_kelurahan = Column(String)
    jenis_kelamin = Column(String)
    jumlah_penduduk = Column(Integer)
    satuan = Column(String)
    tahun = Column(Integer)
