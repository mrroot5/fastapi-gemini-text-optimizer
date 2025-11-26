from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse

from .dependencies import get_query_token
from .routers import products

app = FastAPI(dependencies=[Depends(get_query_token)])


app.include_router(products.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


@app.get("/health")
async def health_check() -> JSONResponse:
    """Health check endpoint for monitoring."""
    return JSONResponse(
        status_code=200,
        content={"status": "healthy", "service": "fastapi-gemini"},
    )
