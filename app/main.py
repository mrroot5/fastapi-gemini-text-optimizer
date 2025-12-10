from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .dependencies import get_query_token
from .routers import products

app = FastAPI(dependencies=[Depends(get_query_token)])


app.include_router(products.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://127.0.0.1:5500",
        "https://mrroot5.github.io",
    ],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check() -> JSONResponse:
    """Health check endpoint for monitoring."""
    return JSONResponse(
        status_code=200,
        content={"status": "healthy", "service": "fastapi-gemini"},
    )
