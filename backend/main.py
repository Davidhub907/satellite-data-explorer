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


