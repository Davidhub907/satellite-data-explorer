import rasterio 

def calculate_statistics(band) -> dict:

    band_min = int(band.min())
    band_max = int(band.max())
    band_mean = float(band.mean())
    band_std = float(band.std())


    results = {

        "min": band_min,
        "max": band_max,
        "mean": band_mean,
        "std": band_std

    }

    return results

with rasterio.open("data/RGB.byte.tif") as src: 

    band = src.read(1)
    nodata = src.nodata
    print(nodata)

    valid_pixels = band[band != nodata]

    stats = calculate_statistics(valid_pixels)
    print(stats)
