export interface Bounds {
  left: number;
  bottom: number;
  right: number;
  top: number;
}

export interface DatasetMetadata {
  filename: string;
  width: number;
  height: number;
  bands: number;
  crs: string;
  resolution: number[];
  bounds: Bounds;
}

export interface BandStatistics {
  band: number;
  min: number;
  max: number;
  mean: number;
  stdDev: number;
}
