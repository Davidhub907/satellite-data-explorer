import rasterio 

def calculate_statistics(band) -> dict:

    band_min = band.min()
    band_max = band.max()
    band_mean = band.mean()
    band_std = band.std()


    results = {

        "min": band_min,
        "max": band_max,
        "mean": band_mean,
        "std": band_std

    }

    return results

with rasterio.open("data/RGB.byte.tif") as src: 

    band = src.read(1)

    stats = calculate_statistics(band)

    print(stats)