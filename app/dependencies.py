from typing import Annotated

from fastapi import Header, HTTPException

from app.config import get_settings


async def get_token_header(x_token: Annotated[str, Header()]) -> None:
    settings = get_settings()

    if x_token != settings.header_token:
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str) -> None:
    settings = get_settings()

    if token != settings.query_token:
        raise HTTPException(
            status_code=400, detail="No query token provided")
