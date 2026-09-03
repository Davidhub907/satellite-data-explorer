# Satellite Data Explorer

A full-stack geospatial raster analysis application built with Python, FastAPI, Rasterio, NumPy, Angular, and TypeScript.

The application discovers raster datasets, analyzes their metadata and pixel statistics through a REST API, and displays the results in an Angular frontend.

I created this project to help me learn and get a basic understanding the languages and the frameworks used in the project. This was not built from scratch, I used ChatGPT and Claude AI to assist in the development. I focused on learning by having AI build out parts of it, then it explained how it worked and why it was important, then I added onto it what I could.

## Features

- Discover available raster datasets
- Select and analyze a dataset
- Display raster dimensions
- Display band count
- Display CRS
- Display resolution
- Display raster bounds
- Calculate per-band minimum, maximum, mean, and standard deviation
- Loading and error states
- Angular frontend connected to a FastAPI backend

## Tech Stack

**Backend**

- Python
- FastAPI
- Rasterio
- NumPy
- Pydantic

**Frontend**

- Angular
- TypeScript
- Angular HttpClient
- RxJS

## Architecture

```text
User
  ↓
Angular Component
  ↓
Angular Service
  ↓
HTTP Request
  ↓
FastAPI
  ↓
Rasterio / NumPy
  ↓
JSON Response
  ↓
Angular UI
```
