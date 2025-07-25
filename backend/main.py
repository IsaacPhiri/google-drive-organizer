# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router as api_router

app = FastAPI()
app.include_router(api_router, prefix="/api")       # Existing API routes

# CORS config: allow React dev and any OAuth callbacks
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://google-drive-organizer-frontend.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
