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

# PyDantic response models

class HealthResponse(BaseModel):
    status: str


class DatasetListResponse(BaseModel):
    total: int
    datasets: list[str]


class Resolution(BaseModel):
    x: float
    y: float


class RasterMetadata(BaseModel):
    width: int
    height: int
    bands: int
    nodata: float | None
    crs: str | None
    resolution: Resolution
    transform: list[float]


class BandStatistics(BaseModel):
    band: int | None = None
    min: int
    max: int
    mean: float
    std: float


class RasterAnalysis(BaseModel):
    metadata: RasterMetadata
    statistics: list[BandStatistics]


# Internal helper functions

def get_dataset_path(dataset: str) -> FilePath:
    dataset_path = (DATA_DIR / dataset).resolve()
    data_directory = DATA_DIR.resolve()

    if dataset_path.parent != data_directory:
        raise HTTPException(
            status_code=400,
            detail="Invalid dataset path",
        )

    if dataset_path.suffix.lower() not in {".tif", ".tiff"}:
        raise HTTPException(
            status_code=400,
            detail="Dataset must be a GeoTIFF file",
        )

    if not dataset_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Dataset '{dataset}' was not found",
        )

    return dataset_path


def run_analysis(dataset: str) -> dict:
    dataset_path = get_dataset_path(dataset)

    try:
        return analyze_raster(str(dataset_path))

    except RasterioIOError:
        raise HTTPException(
            status_code=422,
            detail="The dataset could not be opened as a valid raster",
        )

# API endpoints 

@app.get("/health", response_model=HealthResponse)
def health():
    return {"status": "ok"}


@app.get("/datasets", response_model=DatasetListResponse)
def get_datasets(
    limit: int = Query(default=100, ge=1, le=500)
):
    datasets = sorted(
        file.name
        for file in DATA_DIR.iterdir()
        if file.is_file()
        and file.suffix.lower() in {".tif", ".tiff"}
    )

    return {
        "total": len(datasets),
        "datasets": datasets[:limit],
    }


@app.get("/datasets/{dataset}", response_model=RasterAnalysis)
def get_dataset(
    dataset: str = Path(min_length=1, max_length=255)
):
    return run_analysis(dataset)


@app.get(
    "/datasets/{dataset}/metadata",
    response_model=RasterMetadata,
)
def get_dataset_metadata(
    dataset: str = Path(min_length=1, max_length=255)
):
    analysis = run_analysis(dataset)
    return analysis["metadata"]


@app.get(
    "/datasets/{dataset}/statistics",
    response_model=list[BandStatistics],
)
def get_dataset_statistics(
    dataset: str = Path(min_length=1, max_length=255)
):
    analysis = run_analysis(dataset)
    return analysis["statistics"]