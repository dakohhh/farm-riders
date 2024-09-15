import secure
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware


secure_headers = secure.Secure()


def configure_processes_middleware(app: FastAPI):
    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://127.0.0.1:5500",
            "http://127.0.0.1:3000",
            "http://localhost:3000",
            "http://localhost:3000/",
            "https://farmriders.vercel.app/",
            "https://farmriders.vercel.app",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
