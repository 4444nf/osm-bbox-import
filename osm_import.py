import argparse
import geopandas as gpd
import overpy
from shapely.geometry import LineString, Point
import matplotlib.pyplot as plt
import time
import datetime

def download_osm_gdf_bbox(minlat: float, minlon: float,
                         maxlat: float, maxlon: float,
                         osm_type: str,
                         tag_key: str = None,
                         tag_value: str = None,
                         timeout: int = 180) -> gpd.GeoDataFrame:

    api = overpy.Overpass()

    # tag filter
    if tag_key and tag_value:
        tag_filter = f'["{tag_key}"="{tag_value}"]'
    elif tag_key:
        tag_filter = f'["{tag_key}"]'
    else:
        tag_filter = ""

    # bbox query (area nélkül)
    query = f"""
    [out:json][timeout:{timeout}];
    way["highway"]({minlat},{minlon},{maxlat},{maxlon});
    (._;>;);
    out body;
    """

    result = api.query(query)
    records = []

    if osm_type == "way":
        for way in result.ways:
            coords = [(float(n.lon), float(n.lat)) for n in way.nodes]
            if len(coords) > 1:
                records.append({
                    "geometry": LineString(coords),
                    "osm_id": way.id,
                    **way.tags
                })

    elif osm_type == "node":
        for node in result.nodes:
            records.append({
                "geometry": Point(float(node.lon), float(node.lat)),
                "osm_id": node.id,
                **node.tags
            })

    # üres eset
    if not records:
        return gpd.GeoDataFrame(columns=["geometry"], crs="EPSG:4326")

    return gpd.GeoDataFrame(records, crs="EPSG:4326")

def main():
    parser = argparse.ArgumentParser(description="OSM bbox adatlehívó")
    parser.add_argument("--minlat", type=float, required=True)
    parser.add_argument("--minlon", type=float, required=True)
    parser.add_argument("--maxlat", type=float, required=True)
    parser.add_argument("--maxlon", type=float, required=True)

    parser.add_argument("--type", type=str, required=True,
                        choices=["way", "node"])

    parser.add_argument("--tag_key", type=str)
    parser.add_argument("--tag_value", type=str)

    parser.add_argument("--output", type=str,
                        help="Kimeneti fájl (pl. roads.gpkg vagy roads.shp)")

    parser.add_argument("--plot", action="store_true",
                        help="Kirajzolja matplotlibtel")

    args = parser.parse_args()
    # argumentumok beolvasása

    gdf = download_osm_gdf_bbox(
        minlat=args.minlat,
        minlon=args.minlon,
        maxlat=args.maxlat,
        maxlon=args.maxlon,
        osm_type=args.type,
        tag_key=args.tag_key,
        tag_value=args.tag_value
    )

    print(f"Letöltött elemek száma: {len(gdf)}")

    if args.output:
        gdf.to_file(args.output)
        print(f"Mentve: {args.output}")

    if args.plot and not gdf.empty:
        ax = gdf.plot(figsize=(10, 10))
        ax.set_axis_off()
        plt.show()


if __name__ == "__main__":
    main()

def download_one():
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    gdf = download_osm_gdf_bbox(
        minlat=47.42,
        minlon=19.39,
        maxlat=47.43,
        maxlon=19.40,
        osm_type="way"

    )

    filename = f"osm_data_{ts}.geojson"
    gdf.to_file(filename, driver="GeoJSON")
    print(f"Mentve: {filename}")
