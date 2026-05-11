from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.database import init_db
from app.routes.auth import router as auth_router
from app.routes.events import router as events_router
from app.routes.documents import student_router, teacher_router

DATA_DIR = os.environ.get("DATA_DIR", ".")
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="СтудПортфолио")

# CORS: allow_credentials=False is required when allow_origins=["*"] (browsers
# reject the combination). The frontend uses Bearer tokens, not cookies, so
# credentials aren't needed. If you switch to cookie auth, list explicit origins.
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=False,
                   allow_methods=["*"], allow_headers=["*"])

app.include_router(auth_router)
app.include_router(events_router)
app.include_router(student_router)
app.include_router(teacher_router)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def root():
    return {"status": "ok", "message": "СтудПортфолио API"}
