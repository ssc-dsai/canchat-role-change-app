import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.routes import router
from app.database import database, engine
from app.models import user
from app.config import APP_ENV, APP_NAME, APP_VERSION, API_PREFIX, ALLOWED_ORIGINS

log = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    try:
        await database.connect()
        if APP_ENV == "dev":
            user.create(bind=engine, checkfirst=True)  # Only once at startup
    except Exception as e:
        log.error(f"Failed to connect to database: {e}")
        raise

    yield  # <-- Application runs here

    # --- Shutdown ---
    try:
        await database.disconnect()
    except Exception as e:
        log.error(f"Error disconnecting from database: {e}")
        raise


# Initialize FastAPI app
app = FastAPI(title=APP_NAME, version=APP_VERSION, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix=API_PREFIX)

@app.get("/")
async def root():
    return {
        "name": APP_NAME,
        "version": APP_VERSION
    }