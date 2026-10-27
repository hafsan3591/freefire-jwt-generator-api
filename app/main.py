import os
import logging
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.core import get_jwt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="MEDUSA JWT API",
    description="Free Fire API service",
    version="1.0.0",
)

# Allow requests from your Vercel frontend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://test-jwt-api-medusa.vercel.app",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


class TokenRequest(BaseModel):
    uid: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


@app.get("/")
async def home() -> dict[str, Any]:
    return {
        "status": "online",
        "name": "MEDUSA JWT API",
        "version": "1.0.0",
        "docs": "/docs",
        "message": "API service is running",
    }


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/token")
async def get_token_get(
    uid: str = Query(..., min_length=1),
    password: str = Query(..., min_length=1),
) -> dict[str, Any]:
    return await generate_token(uid, password)


@app.post("/api/token")
async def get_token_post(data: TokenRequest) -> dict[str, Any]:
    return await generate_token(data.uid, data.password)


async def generate_token(
    uid: str,
    password: str,
) -> dict[str, Any]:
    try:
        # Call the existing project function.
        result = await get_jwt(uid, password)

        if isinstance(result, dict):
            return result

        return {
            "status": "success",
            "token": result,
        }

    except HTTPException:
        raise

    except Exception as exc:
        # Keep credentials and internal details out of public responses.
        logger.error(
            "Token generation failed for a request: %s",
            type(exc).__name__,
        )
        raise HTTPException(
            status_code=502,
            detail="Token generation failed. Check server logs.",
        ) from NoneNone
