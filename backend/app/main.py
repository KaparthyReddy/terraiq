from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.api.routes import auth, fields, sensors, recommendations, satellite
from app.core.config import settings
from app.core.logging import setup_logging
from app.db.session import engine
from app.db.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="TerraIQ API",
    description="AI-powered soil health intelligence platform",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

app.include_router(auth.router,            prefix="/api/v1/auth",            tags=["auth"])
app.include_router(fields.router,          prefix="/api/v1/fields",          tags=["fields"])
app.include_router(sensors.router,         prefix="/api/v1/sensors",         tags=["sensors"])
app.include_router(recommendations.router, prefix="/api/v1/recommendations", tags=["recommendations"])
app.include_router(satellite.router,       prefix="/api/v1/satellite",       tags=["satellite"])


@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}
