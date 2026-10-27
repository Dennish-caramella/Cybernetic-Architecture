"""Scarico da OpenStreetMap (osmnx). Richiede rete verso overpass/nominatim: da eseguire sulla macchina dell'autore.

I tag usati per le categorie di servizio sono scelte di modellazione, non verità: la completezza dei tag a Milano
va verificata (confronto con elenchi ufficiali, es. scuole e farmacie) prima di citare i risultati.
"""
from pathlib import Path

import geopandas as gpd
import osmnx as ox

from .io_utils import WGS84

POI_TAGS = {
    "metro": {"railway": ["subway_entrance", "station", "halt"]},
    "scuola": {"amenity": ["school"]},
    "asilo": {"amenity": ["kindergarten", "childcare"]},
    "sanita": {"amenity": ["hospital", "clinic", "doctors"]},
    "farmacia": {"amenity": ["pharmacy"]},
    "verde": {"leisure": ["park", "garden", "playground"]},
    "commercio": {"shop": ["supermarket", "convenience"]},
}
TRANSFORM_TAGS = {"landuse": ["brownfield", "railway", "industrial", "construction", "military"]}
PROTECTED_TAGS = {"boundary": ["protected_area"], "leisure": ["nature_reserve"]}


def _cache(cache_dir, name):
    return Path(cache_dir) / name


def fetch_boundary(query, cache_dir):
    f = _cache(cache_dir, "confine.gpkg")
    if f.exists():
        return gpd.read_file(f)
    g = ox.geocode_to_gdf(query).to_crs(WGS84)[["geometry"]]
    Path(cache_dir).mkdir(parents=True, exist_ok=True)
    g.to_file(f, driver="GPKG")
    return g


def fetch_graph(polygon, cache_dir):
    f = _cache(cache_dir, "walk.graphml")
    if f.exists():
        return ox.load_graphml(f)
    G = ox.graph_from_polygon(polygon, network_type="walk", simplify=True)
    ox.save_graphml(G, f)
    return G


def fetch_features(polygon, tags, cache_dir, name):
    f = _cache(cache_dir, f"{name}.gpkg")
    if f.exists():
        return gpd.read_file(f)
    try:
        g = ox.features_from_polygon(polygon, tags)
    except Exception as e:  # nessun elemento trovato oppure errore di rete
        print(f"osm {name}: {e}")
        return gpd.GeoDataFrame({"geometry": []}, crs=WGS84)
    g = g.reset_index(drop=True)[["geometry"] + [c for c in tags if c in g.columns]]
    g.to_file(f, driver="GPKG")
    return g


def fetch_all(boundary, cache_dir):
    poly = boundary.union_all()
    out = {"graph": fetch_graph(poly, cache_dir), "pois": {}}
    for cat, tags in POI_TAGS.items():
        g = fetch_features(poly, tags, cache_dir, f"poi_{cat}")
        g = g[g.geometry.notna()].copy()
        g["geometry"] = g.geometry.representative_point()
        out["pois"][cat] = g
    out["buildings"] = fetch_features(poly, {"building": True}, cache_dir, "edifici")
    out["transform"] = fetch_features(poly, TRANSFORM_TAGS, cache_dir, "landuse_dismessi")
    out["protected"] = fetch_features(poly, PROTECTED_TAGS, cache_dir, "protette")
    return out


def fetch_major_roads(boundary, cache_dir):
    """Solo per lo sfondo del viewer: strade principali (non usate nei calcoli)."""
    f = _cache(cache_dir, "strade_principali.gpkg")
    if f.exists():
        return gpd.read_file(f)
    try:
        G = ox.graph_from_polygon(boundary.union_all(), custom_filter='["highway"~"motorway|trunk|primary|secondary"]', simplify=True)
        e = ox.graph_to_gdfs(G, nodes=False).reset_index(drop=True)[["geometry"]]
    except Exception as ex:
        print("strade principali:", ex)
        return gpd.GeoDataFrame({"geometry": []}, crs=WGS84)
    e.to_file(f, driver="GPKG")
    return e
