from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from app.db import SessionLocal, engine  # Pastikan import dari path yang benar
from app import models  # Mengimpor models dari app
from app.api.routes import penduduk  # Mengimpor routes dari subfolder api.routes

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

# Include routers
app.include_router(penduduk.router, prefix="/penduduk", tags=["Penduduk"])

# Menyajikan file statis
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# @app.get("/")
# async def read_root():
#     return {"message": "Hello World"}
