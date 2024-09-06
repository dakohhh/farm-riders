import secure
from fastapi import Request, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware


secure_headers = secure.Secure()


def configure_processes_middleware(app: FastAPI):

    # CORS Middleware
    app.add_middleware(
        CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
    )

    app.add_middleware(GZipMiddleware, minimum_size=1000)

    @app.middleware("http")
    async def set_secure_headers(request, call_next):
        response = await call_next(request)
        secure_headers.framework.fastapi(response)
        return response
