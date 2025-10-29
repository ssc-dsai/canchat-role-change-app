import logging
from pydantic import EmailStr
from fastapi import FastAPI, HTTPException, Header, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager

from app.routes import router
from app.database import database, engine
from app.models import user
from app.config import APP_ENV, APP_NAME, APP_NAME_FR, APP_VERSION, APP_PREFIX, API_PREFIX, ALLOWED_ORIGINS, ALLOWED_ROLES

log = logging.getLogger(__name__)

templates = Jinja2Templates(directory="app/templates")  # Initialize Jinja2 templates

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
app = FastAPI(title=APP_NAME, version=APP_VERSION, lifespan=lifespan, root_path=APP_PREFIX)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix=API_PREFIX)

@app.get("/", response_class=HTMLResponse)  # Specify the response class
async def root(request: Request, x_forwarded_email: EmailStr = Header(None)):

    if not x_forwarded_email:
        return templates.TemplateResponse("403.html", {"request": request})  # Render the 403 template
    
    return templates.TemplateResponse("index.html", {"request": request, "email": x_forwarded_email, "app_name": APP_NAME, "allowed_roles": ALLOWED_ROLES})  # Render the template

@app.get("/fr", response_class=HTMLResponse)  # Specify the response class
async def root(request: Request, x_forwarded_email: EmailStr = Header(None)):

    if not x_forwarded_email:
        return templates.TemplateResponse("403.html", {"request": request})  # Render the 403 template
    
    return templates.TemplateResponse("index_fr.html", {"request": request, "email": x_forwarded_email, "app_name": APP_NAME_FR, "allowed_roles": ALLOWED_ROLES})  # Render the template


@app.get("/health")
async def healthcheck():
    return {"status": True}

@app.get("/health/db")
async def healthcheck_with_db():
    try:
        query = user.select().limit(1)
        await database.fetch_one(query)        
        return {"status": True}
    except Exception as e:
        log.error(f"Database health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed",
        )
