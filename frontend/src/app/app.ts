import { Component, inject, OnInit } from '@angular/core';

import { forkJoin } from 'rxjs';

import { DatasetService } from './dataset.service';

import { BandStatistics, DatasetMetadata } from './dataset';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App implements OnInit {
  private datasetService = inject(DatasetService);

  title = 'Satellite Data Explorer';

  datasets: string[] = [];

  selectedDataset = '';

  metadata: DatasetMetadata | null = null;

  statistics: BandStatistics[] = [];

  loadingDatasets = true;

  analyzing = false;

  error = '';

  ngOnInit(): void {
    this.loadDatasets();
  }

  loadDatasets(): void {
    this.loadingDatasets = true;
    this.error = '';

    this.datasetService.getDatasets().subscribe({
      next: (datasets) => {
        this.datasets = datasets;

        if (datasets.length > 0) {
          this.selectedDataset = datasets[0];
        }

        this.loadingDatasets = false;
      },

      error: (error) => {
        console.error(error);

        this.error = 'Could not load datasets from the backend.';

        this.loadingDatasets = false;
      },
    });
  }

  selectDataset(dataset: string): void {
    this.selectedDataset = dataset;

    this.metadata = null;
    this.statistics = [];
    this.error = '';
  }

  analyzeDataset(): void {
    if (!this.selectedDataset) {
      return;
    }

    this.analyzing = true;

    this.error = '';

    this.metadata = null;
    this.statistics = [];

    forkJoin({
      metadata: this.datasetService.getMetadata(this.selectedDataset),

      statistics: this.datasetService.getStatistics(this.selectedDataset),
    }).subscribe({
      next: (result) => {
        this.metadata = result.metadata;

        this.statistics = result.statistics;

        this.analyzing = false;
      },

      error: (error) => {
        console.error(error);

        this.error = 'An error occurred while analyzing the dataset.';

        this.analyzing = false;
      },
    });
  }
}
