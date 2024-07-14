from fastapi import APIRouter, Depends, HTTPException, Header, Request, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db import SessionLocal
from app.models import Penduduk
from fastapi.responses import JSONResponse

router = APIRouter()

def get_models():
    from . import models, schemas
    return models, schemas

def get_db(request: Request):
    return request.state.db

@router.get("/all")
async def get_all(db: Session = Depends(get_db)):
    # if token != "xYEq9m2f8C8X4F9fZvp2QbndsPfESunN":
    #     raise HTTPException(status_code=403, detail="Invalid token")
    
    # Mengambil semua data penduduk perkecamatan dan kelurahan serta menghitung jumlah penduduk berdasarkan jenis kelamin
    penduduk_list = db.query(
        Penduduk.nama_kecamatan,
        Penduduk.nama_kelurahan,
        Penduduk.jenis_kelamin,
        func.sum(Penduduk.jumlah_penduduk).label("jumlah_penduduk")
    ).group_by(Penduduk.nama_kecamatan, Penduduk.nama_kelurahan, Penduduk.jenis_kelamin).all()
    
    data = {}
    total_laki_laki = 0
    total_perempuan = 0

    for kecamatan, kelurahan, jenis_kelamin, jumlah_penduduk in penduduk_list:
        if kecamatan not in data:
            data[kecamatan] = {
                "kelurahan": {},
                "laki_laki_per_kecamatan": 0,
                "perempuan_per_kecamatan": 0,
                "total_penduduk_per_kecamatan": 0
            }
        
        if kelurahan not in data[kecamatan]["kelurahan"]:
            data[kecamatan]["kelurahan"][kelurahan] = {
                "laki_laki_per_kelurahan": 0,
                "perempuan_per_kelurahan": 0,
                "total_penduduk_per_kelurahan": 0
            }

        if jenis_kelamin.lower() == 'laki-laki':
            data[kecamatan]["kelurahan"][kelurahan]["laki_laki_per_kelurahan"] += jumlah_penduduk
            data[kecamatan]["laki_laki_per_kecamatan"] += jumlah_penduduk
            total_laki_laki += jumlah_penduduk
        else:
            data[kecamatan]["kelurahan"][kelurahan]["perempuan_per_kelurahan"] += jumlah_penduduk
            data[kecamatan]["perempuan_per_kecamatan"] += jumlah_penduduk
            total_perempuan += jumlah_penduduk
        
        data[kecamatan]["kelurahan"][kelurahan]["total_penduduk_per_kelurahan"] += jumlah_penduduk
        data[kecamatan]["total_penduduk_per_kecamatan"] += jumlah_penduduk
    
    total_penduduk = total_laki_laki + total_perempuan
    
    return {
        "data": data,
        "total_laki_laki": total_laki_laki,
        "total_perempuan": total_perempuan,
        "total_penduduk": total_penduduk
    }

@router.get("/kecamatan")
async def get_kecamatan(token: str = Header(...), nama_kecamatan: str = Query(None), db: Session = Depends(get_db)):
    if token != "xYEq9m2f8C8X4F9fZvp2QbndsPfESunN":
        raise HTTPException(status_code=403, detail="Invalid token")
    
    # Mengambil semua data penduduk perkecamatan dan kelurahan serta menghitung jumlah penduduk berdasarkan jenis kelamin
    query = db.query(
        Penduduk.nama_kecamatan,
        Penduduk.jenis_kelamin,
        func.sum(Penduduk.jumlah_penduduk).label("jumlah_penduduk")
    )
    
    if nama_kecamatan:
        query = query.filter(Penduduk.nama_kecamatan == nama_kecamatan)
    
    penduduk_list = query.group_by(Penduduk.nama_kecamatan, Penduduk.jenis_kelamin).all()
    
    data = {}

    for kecamatan, jenis_kelamin, jumlah_penduduk in penduduk_list:
        if kecamatan not in data:
            data[kecamatan] = {
                "laki_laki": 0,
                "perempuan": 0,
                "total_penduduk": 0
            }

        if jenis_kelamin.lower() == 'laki-laki':
            data[kecamatan]["laki_laki"] += jumlah_penduduk
        else:
            data[kecamatan]["perempuan"] += jumlah_penduduk
        
        data[kecamatan]["total_penduduk"] += jumlah_penduduk
        
    return {
        "data": data
    }

@router.get("/kelurahan")
async def get_kelurahan(
    token: str = Header(...),
    nama_kelurahan: str = Query(None),
    db: Session = Depends(get_db)
):
    if token != "xYEq9m2f8C8X4F9fZvp2QbndsPfESunN":
        raise HTTPException(status_code=403, detail="Invalid token")

    # Mengambil data penduduk berdasarkan kecamatan dan kelurahan serta menghitung jumlah penduduk berdasarkan jenis kelamin
    query = db.query(
        Penduduk.nama_kecamatan,
        Penduduk.nama_kelurahan,
        Penduduk.jenis_kelamin,
        func.sum(Penduduk.jumlah_penduduk).label("jumlah_penduduk")
    )
    
    if nama_kelurahan:
        query = query.filter(Penduduk.nama_kelurahan == nama_kelurahan)
    
    penduduk_list = query.group_by(Penduduk.nama_kecamatan, Penduduk.nama_kelurahan, Penduduk.jenis_kelamin).all()

    data = {}

    for kecamatan, kelurahan, jenis_kelamin, jumlah_penduduk in penduduk_list:
        # if kecamatan not in data:
        #     data[kecamatan] = {
        #         "kelurahan": {},
        #     }

        if kelurahan not in data:
            data[kelurahan] = {
                "kecamatan": kecamatan,
                "laki_laki": 0,
                "perempuan": 0,
                "total_penduduk": 0
            }

        if jenis_kelamin.lower() == 'laki-laki':
            data[kelurahan]["laki_laki"] += jumlah_penduduk
        else:
            data[kelurahan]["perempuan"] += jumlah_penduduk
        
        data[kelurahan]["total_penduduk"] += jumlah_penduduk

    return {
        "data": data
    }