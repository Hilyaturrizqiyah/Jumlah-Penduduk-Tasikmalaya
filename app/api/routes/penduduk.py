from fastapi import APIRouter, Depends, HTTPException, Header, Request, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db import SessionLocal
from app.models import Penduduk
from fastapi.responses import JSONResponse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

def get_models():
    from . import models, schemas
    return models, schemas

def get_db(request: Request):
    return request.state.db

@router.get("/all")
async def get_all(db: Session = Depends(get_db)):
    
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
    
    if nama_kecamatan and nama_kecamatan != "All":
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
    nama_kelurahan: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    if token != "xYEq9m2f8C8X4F9fZvp2QbndsPfESunN":
        raise HTTPException(status_code=403, detail="Invalid token")

    logger.info(f"Received request for kelurahan: {nama_kelurahan}")

    query = db.query(
        Penduduk.nama_kecamatan,
        Penduduk.nama_kelurahan,
        Penduduk.jenis_kelamin,
        func.sum(Penduduk.jumlah_penduduk).label("jumlah_penduduk")
    ).filter(Penduduk.nama_kelurahan == nama_kelurahan.strip())

    penduduk_list = query.group_by(Penduduk.nama_kecamatan, Penduduk.nama_kelurahan, Penduduk.jenis_kelamin).all()

    if not penduduk_list:
        logger.warning(f"No data found for kelurahan: {nama_kelurahan}")
        raise HTTPException(status_code=404, detail=f"No data found for kelurahan: {nama_kelurahan}")

    data = {}

    for kecamatan, kelurahan, jenis_kelamin, jumlah_penduduk in penduduk_list:
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

    logger.info(f"Final data for kelurahan {nama_kelurahan}: {data}")

    return {
        "data": data
    }


@router.get("/kecamatan_list")
async def get_kecamatan_list(token: str = Header(...), db: Session = Depends(get_db)):
    if token != "xYEq9m2f8C8X4F9fZvp2QbndsPfESunN":
        raise HTTPException(status_code=403, detail="Invalid token")

    kecamatan_list = db.query(Penduduk.nama_kecamatan).distinct().all()
    return {"kecamatan": [k.nama_kecamatan for k in kecamatan_list]}

@router.get("/kelurahan_list")
async def get_kelurahan_list(token: str = Header(...), kecamatan: str = Query(None), db: Session = Depends(get_db)):
    if token != "xYEq9m2f8C8X4F9fZvp2QbndsPfESunN":
        raise HTTPException(status_code=403, detail="Invalid token")

    kelurahan_list = db.query(Penduduk.nama_kelurahan).filter(Penduduk.nama_kecamatan == kecamatan).distinct().all()
    return {"kelurahan": [k.nama_kelurahan for k in kelurahan_list]}