from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from .core import config
from .api import rates
from .api import etl

# Initialize FastAPI app
app = FastAPI(
    title="EGP Currency Converter API",
    description="API for historical currency exchange rate conversions and ETL management.",
    version="1.0.0",
)

# CORS configuration
origins = config.CORS_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,                                  # Allowed origins from .env
    allow_credentials=False if "*" in origins else True,    # Credentials only if not using '*'
    allow_methods=["*"],                                    # Allow all methods
    allow_headers=["*"],                                    # Allow all headers
)

# Include API routers
app.include_router(rates.router, prefix="/currency", tags=["Currency Conversion"])
app.include_router(etl.router, prefix="/etl", tags=["ETL Management"])

# Redirect root to docs
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

# Health check endpoint
@app.get("/health", tags=["Monitoring"])
async def health_check():
    return {"status": "ok", "message": "API is running successfully!"}
