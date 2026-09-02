import rasterio 

def calculate_statistic(band) -> dict: 
    band_max = int(band.max())
    band_min = int(band.min())
    band_mean = float(band.mean())
    band_std = float(band.std())

    results =  {

        "Max": band_max,
        "Min": band_min,
        "Mean": band_mean,
        "Std": band_std
    }

    return results

def calculate_metadata(src) -> dict:
    width = int(src.width)
    height = int(src.height)
    amount = int(src.count)
    nodata = (src.nodata)

    results = {

        "Width": width,
        "Height": height,
        "Bands": amount,
        "Nodata": nodata
        
    }

    return results


def analyze_raster(file_path):

    with rasterio.open(file_path) as src:

        band = src.read(1)
        nodata = src.nodata

        if nodata is not None:
            valid_pixels = band[band != nodata]
        else:
            valid_pixels = band

        stats = calculate_statistic(valid_pixels)
        metadata = calculate_metadata(src)

        results = {

            "metadata": metadata,
            "statistics": stats
        }

        return results




results = analyze_raster("data/RGB.byte.tif")
print(results)