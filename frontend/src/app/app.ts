import { Component, signal } from '@angular/core';

@Component({
  selector: 'app-root',
  imports: [],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {
  title = 'Satellite Data Explorer';
  filename = 'landsat_sample.tif';
  width = 2048;
  height = 2048;
  bands = 4;
}
