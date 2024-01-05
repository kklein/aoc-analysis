from pathlib import Path

import click
import matplotlib.pyplot as plt
import pandas as pd
from git_root import git_root

_N_REPOS = "n_repos"
_Q_REPOS = "q_repos"


def _load_data(path: Path) -> pd.DataFrame:
    df = pd.read_json(path, orient="index")
    df.columns = [_N_REPOS]
    df[_Q_REPOS] = df[_N_REPOS] / df[_N_REPOS].sum()
    return df


def _histogram(df: pd.DataFrame, filename: str = "languages.png", n_languages: int = 20) -> None:
    n = df[_N_REPOS].sum()

    fig, ax = plt.subplots(figsize=(9, 6))

    df.sort_values(_N_REPOS, ascending=False).iloc[:n_languages].plot.bar(y=_Q_REPOS, ax=ax)

    ax.set_ylabel("fraction of repositories")
    ax.set_title(f"Which programming language was used how often? (n={n})")
    ax.get_legend().remove()

    fig.tight_layout()
    filepath = Path(git_root()) / filename
    fig.savefig(filepath)
    print(f"Saved file to {filepath}.")


@click.command()
@click.argument("data_dir", type=click.Path(exists=True))
def main_cli(data_dir):
    path = Path(data_dir) / "languages.json"
    df_languages = _load_data(path)
    _histogram(df_languages)


if __name__ == "__main__":
    main_cli()
