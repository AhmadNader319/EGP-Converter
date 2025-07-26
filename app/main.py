# app/main.py
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import os # Import os for potential environment variable usage or path handling

# Import the APIRouter instances from your api sub-package
# Ensure these files (rates.py, etl.py) exist in app/api/
from .api import rates
from .api import etl

# Initialize the FastAPI application
app = FastAPI(
    title="EGP Currency Converter API",
    description="API for historical currency exchange rate conversions and ETL management.",
    version="1.0.0",
    # You can customize documentation URLs or disable them if needed
    # docs_url="/documentation",
    # redoc_url=None,
)

# Router for currency conversion endpoints
app.include_router(rates.router, prefix="/currency", tags=["Currency Conversion"])

# Router for ETL management endpoints
app.include_router(etl.router, prefix="/etl", tags=["ETL Management"])

# Optional: Add a root endpoint to redirect directly to the OpenAPI documentation
@app.get("/", include_in_schema=False)
async def root():
    """
    Redirects to the OpenAPI (Swagger UI) documentation for the API.
    """
    return RedirectResponse(url="/docs")

# Optional: Add a simple health check endpoint
@app.get("/health", tags=["Monitoring"])
async def health_check():
    """
    Provides a simple health check to indicate if the API is running.
    """
    return {"status": "ok", "message": "API is running successfully!"}
