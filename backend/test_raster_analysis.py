import rasterio

from backend.raster_analysis import calculate_metadata


TEST_RASTER = "data/RGB.byte.tif"


def test_metadata():
    with rasterio.open(TEST_RASTER) as src:
        metadata = calculate_metadata(src)

    assert metadata["width"] == 791
    assert metadata["height"] == 718
    assert metadata["bands"] == 3
    assert metadata["crs"] == "EPSG:32618"

    assert "resolution" in metadata
    assert metadata["resolution"]["x"] > 0
    assert metadata["resolution"]["y"] > 0

    assert "bounds" in metadata
    assert metadata["bounds"]["left"] != 0
    assert metadata["bounds"]["right"] != 0