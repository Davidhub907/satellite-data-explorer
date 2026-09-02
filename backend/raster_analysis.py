import rasterio 

def calculate_statistic(band) -> dict: 

    band_max = int(band.max())
    band_min = int(band.min())
    band_mean = float(band.mean())
    band_std = float(band.std())

    results =  {

        "band": None,
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

        nodata = src.nodata

        metadata = calculate_metadata(src)

        band_statistics = []

        for band_number in range(1, src.count + 1):

            current_band = src.read(band_number)

            if nodata is not None:
                valid_pixels = current_band[current_band != nodata]
            else:
                valid_pixels = current_band

            stats = calculate_statistic(valid_pixels) 
            stats["band"] = band_number
            band_statistics.append(stats)           

        results = {

            "metadata": metadata,
            "statistics": band_statistics

        }

        return results




results = analyze_raster("data/RGB.byte.tif")
print(results)