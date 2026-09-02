from pathlib import Path as FilePath

from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rasterio.errors import RasterioIOError

from backend.raster_analysis import analyze_raster

DATA_DIR = FilePath(__file__).resolve().parent.parent / "data"

app = FastAPI(
    title="Satellite Data Explorer API",
    description="REST API for analyzing GeoTIFF satellite datasets",
    version="0.1.0",
)


# CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)