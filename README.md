# OSM BBox Importer

This Python script allows you to download OpenStreetMap (OSM) data for a given bounding box (latitude/longitude) using the Overpass API. 

## Features

- Download OSM data by bounding box.
- Support for `way` and `node` types.
- Optional filtering by `tag_key` and `tag_value`.
- Output to GeoPackage, Shapefile, or GeoJSON.
- Optional plotting with Matplotlib.
- Fully configurable from the command line using `argparse`.

## Requirements

- Python 3.8+
- `geopandas`
- `overpy`
- `shapely`
- `matplotlib`

## Usage

```bash
python script.py --minlat 47.42 --minlon 19.39 --maxlat 47.43 --maxlon 19.40 --type way --output roads.gpkg --plot
