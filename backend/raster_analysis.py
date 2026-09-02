import rasterio


def calculate_statistics(band) -> dict:
    """Calculate summary statistics for valid raster pixels."""

    return {
        "min": int(band.min()),
        "max": int(band.max()),
        "mean": float(band.mean()),
        "std": float(band.std()),
    }


def calculate_metadata(src) -> dict:
    """Extract useful metadata from an opened Rasterio dataset."""

    return {
        "width": src.width,
        "height": src.height,
        "bands": src.count,
        "nodata": src.nodata,
        "crs": str(src.crs) if src.crs else None,
        "resolution": {
            "x": float(src.res[0]),
            "y": float(src.res[1]),
        },
        "transform": list(src.transform),
    }


def analyze_raster(file_path: str) -> dict:
    """Analyze a GeoTIFF and return metadata and statistics for every band."""

    with rasterio.open(file_path) as src:

        metadata = calculate_metadata(src)
        band_statistics = []

        for band_number in range(1, src.count + 1):

            band = src.read(band_number)
            nodata = src.nodata

            if nodata is not None:
                valid_pixels = band[band != nodata]
            else:
                valid_pixels = band

            stats = calculate_statistics(valid_pixels)
            stats["band"] = band_number

            band_statistics.append(stats)

        return {
            "metadata": metadata,
            "statistics": band_statistics,
        }


if __name__ == "__main__":
    results = analyze_raster("data/RGB.byte.tif")
    print(results)