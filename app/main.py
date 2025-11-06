from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, products, users

app = FastAPI(dependencies=[Depends(get_query_token)])


# app.include_router(users.router)
# app.include_router(items.router)
app.include_router(products.router)
# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )


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
