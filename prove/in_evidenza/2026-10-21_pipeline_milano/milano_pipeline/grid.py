import geopandas as gpd
import h3
from shapely.geometry import Polygon

from .io_utils import METRIC, WGS84


def build_grid(boundary_gdf, res):
    """Celle H3 che intersecano il confine, ritagliate al confine (area_m2 = area DENTRO il confine). h3.geo_to_cells include solo le celle con il centro dentro il poligono:
    si espande il confine di una cella e poi si filtra per intersezione, così le celle di bordo non si perdono."""
    geom = boundary_gdf.to_crs(WGS84).union_all()
    edge = h3.average_hexagon_edge_length(res, "m")
    buffered = (
        gpd.GeoSeries([geom], crs=WGS84).to_crs(METRIC).buffer(2 * edge).to_crs(WGS84).iloc[0]
    )
    cells = set()
    polys = [buffered] if buffered.geom_type == "Polygon" else list(buffered.geoms)
    for p in polys:
        cells |= set(h3.geo_to_cells(p.__geo_interface__, res))
    rows = []
    for c in sorted(cells):
        ring = [(lng, lat) for lat, lng in h3.cell_to_boundary(c)]
        poly = Polygon(ring)
        if poly.intersects(geom):
            clipped = poly.intersection(geom)       # le celle di bordo sono ritagliate al confine
            if not clipped.is_empty and clipped.area > 0:
                rows.append({"h3": c, "geometry": clipped})
    g = gpd.GeoDataFrame(rows, geometry="geometry", crs=WGS84)
    g["area_m2"] = g.to_crs(METRIC).area
    return g


def cell_centroids(grid):
    c = grid.to_crs(METRIC).centroid
    return gpd.GeoDataFrame({"h3": grid["h3"].values}, geometry=c, crs=METRIC).to_crs(WGS84)
