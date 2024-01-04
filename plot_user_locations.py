from pathlib import Path

import click
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import requests
from dotenv import dotenv_values
from git_root import git_root

_MAPS_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"


def _api_key() -> str:
    api_key = dotenv_values(".env")["API_KEY"]
    if not api_key:
        raise ValueError()
    return api_key


def coordinates_for_location(location: str, base_url: str = _MAPS_BASE_URL) -> dict:
    params = {"key": _api_key(), "address": location}
    response = requests.get(base_url, params=params)
    try:
        return response.json()["results"][0]["geometry"]["location"]
    # This is kind of nasty
    except:
        return {}


def coordinates_for_locations(path: Path) -> pd.DataFrame:
    coordinates_list = []
    for child in path.iterdir():
        with open(child) as filehandle:
            location = filehandle.readline()
        if location != "\n":
            coordinates_list.append(coordinates_for_location(location))
    print(f"Identified {len(coordinates_list)} coordinates.")
    return pd.DataFrame(coordinates_list)


def plot_locations(df: pd.DataFrame, filename: str = "worldmap.png") -> None:
    fig, ax = plt.subplots(figsize=(20, 10))
    countries = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    countries.plot(color="lightgrey", ax=ax)
    df.plot(
        x="lng",
        y="lat",
        kind="scatter",
        colormap="YlOrRd",
        ax=ax,
        s=100,
    )
    filepath = Path(git_root()) / filename
    fig.savefig(filepath)
    print(f"Saved file to {filepath}.")


@click.command()
@click.argument("data_dir", type=click.Path(exists=True))
def main_cli(data_dir):
    path = Path(data_dir)
    coordinates = coordinates_for_locations(path)
    plot_locations(coordinates)


if __name__ == "__main__":
    main_cli()
