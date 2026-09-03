import { Component, inject, OnInit, signal } from '@angular/core';

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

  datasets = signal<string[]>([]);

  selectedDataset = signal('');

  metadata = signal<DatasetMetadata | null>(null);

  statistics = signal<BandStatistics[]>([]);

  loadingDatasets = signal(true);

  analyzing = signal(false);

  error = signal('');

  ngOnInit(): void {
    this.loadDatasets();
  }

  loadDatasets(): void {
    this.loadingDatasets.set(true);
    this.error.set('');

    this.datasetService.getDatasets().subscribe({
      next: (datasets) => {
        console.log('Datasets received:', datasets);

        this.datasets.set(datasets);

        if (datasets.length > 0) {
          this.selectedDataset.set(datasets[0]);
        }

        this.loadingDatasets.set(false);
      },

      error: (error) => {
        console.error('Dataset loading error:', error);

        this.error.set('Could not load datasets from the backend.');

        this.loadingDatasets.set(false);
      },
    });
  }

  selectDataset(dataset: string): void {
    this.selectedDataset.set(dataset);

    this.metadata.set(null);
    this.statistics.set([]);
    this.error.set('');
  }

  analyzeDataset(): void {
    const dataset = this.selectedDataset();

    if (!dataset) {
      return;
    }

    this.analyzing.set(true);
    this.error.set('');

    this.metadata.set(null);
    this.statistics.set([]);

    forkJoin({
      metadata: this.datasetService.getMetadata(dataset),

      statistics: this.datasetService.getStatistics(dataset),
    }).subscribe({
      next: (result) => {
        this.metadata.set(result.metadata);
        this.statistics.set(result.statistics);

        this.analyzing.set(false);
      },

      error: (error) => {
        console.error('Analysis error:', error);

        this.error.set('An error occurred while analyzing the dataset.');

        this.analyzing.set(false);
      },
    });
  }
}
