import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map, Observable } from 'rxjs';

import { BandStatistics, DatasetMetadata } from './dataset';
@Injectable({
  providedIn: 'root',
})
export class DatasetService {
  private http = inject(HttpClient);

  private readonly apiUrl = 'http://127.0.0.1:8000';

  getDatasets(): Observable<string[]> {
    return this.http.get<any>(`${this.apiUrl}/datasets`).pipe(
      map((response) => {
        if (Array.isArray(response)) {
          return response;
        }

        return response.datasets ?? [];
      }),
    );
  }

  getMetadata(dataset: string): Observable<DatasetMetadata> {
    const encodedDataset = encodeURIComponent(dataset);

    return this.http
      .get<any>(`${this.apiUrl}/datasets/${encodedDataset}/metadata`)
      .pipe(map((data) => this.normalizeMetadata(data, dataset)));
  }

  getStatistics(dataset: string): Observable<BandStatistics[]> {
    const encodedDataset = encodeURIComponent(dataset);

    return this.http
      .get<any>(`${this.apiUrl}/datasets/${encodedDataset}/statistics`)
      .pipe(map((data) => this.normalizeStatistics(data)));
  }

  private normalizeMetadata(data: any, dataset: string): DatasetMetadata {
    const rawBounds = data.bounds;

    let bounds;

    if (Array.isArray(rawBounds)) {
      bounds = {
        left: Number(rawBounds[0]),
        bottom: Number(rawBounds[1]),
        right: Number(rawBounds[2]),
        top: Number(rawBounds[3]),
      };
    } else {
      bounds = {
        left: Number(rawBounds?.left ?? 0),
        bottom: Number(rawBounds?.bottom ?? 0),
        right: Number(rawBounds?.right ?? 0),
        top: Number(rawBounds?.top ?? 0),
      };
    }

    const resolution = Array.isArray(data.resolution)
      ? data.resolution
      : [Number(data.resolution?.x ?? 0), Number(data.resolution?.y ?? 0)];

    return {
      filename: data.filename ?? dataset,
      width: Number(data.width),
      height: Number(data.height),
      bands: Number(data.bands ?? data.count),
      crs: String(data.crs ?? 'Unknown'),
      resolution,
      bounds,
    };
  }

  private normalizeStatistics(data: any): BandStatistics[] {
    let rows: any[] = [];

    if (Array.isArray(data)) {
      rows = data;
    } else if (Array.isArray(data.statistics)) {
      rows = data.statistics;
    } else if (Array.isArray(data.bands)) {
      rows = data.bands;
    } else if (data.min !== undefined || data.minimum !== undefined) {
      rows = [data];
    } else if (data && typeof data === 'object') {
      rows = Object.entries(data)
        .filter(([, value]) => value !== null && typeof value === 'object')
        .map(([key, value], index) => {
          const stat = value as any;

          const bandNumber = Number(key.match(/\d+/)?.[0]) || index + 1;

          return {
            ...stat,
            band: stat.band ?? bandNumber,
          };
        });
    }

    return rows.map((stat, index) => ({
      band: Number(stat.band ?? index + 1),

      min: Number(stat.min ?? stat.minimum ?? stat.band_min ?? 0),

      max: Number(stat.max ?? stat.maximum ?? stat.band_max ?? 0),

      mean: Number(stat.mean ?? stat.band_mean ?? 0),

      stdDev: Number(stat.stdDev ?? stat.std_dev ?? stat.std ?? stat.standard_deviation ?? 0),
    }));
  }
}
