from .penduduk import router as penduduk_router

from fastapi import APIRouter

router = APIRouter()
router.include_router(penduduk_router)
