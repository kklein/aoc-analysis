from pathlib import Path

import click
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from git_root import git_root

_N_SUBMISSIONS = "n_submissions"
_Q_SUBMISSIONS = "q_submissions"


DfDict = dict[int, pd.DataFrame]


def _load_data(path: Path) -> DfDict:
    dfs = {}
    # TODO: Infer years by loading all available csv files.
    for year in [2021, 2022, 2023]:
        dfs[year] = pd.read_csv(
            path / f"{year}.csv", index_col="day", sep=","
        ).sort_index()
        dfs[year][_Q_SUBMISSIONS] = (
            dfs[year][_N_SUBMISSIONS] / dfs[year][_N_SUBMISSIONS].iloc[0]
        )
    return dfs


def _plot_absolute(
    dfs: DfDict, ax_linear: matplotlib.axes.Axes, ax_log: matplotlib.axes.Axes
) -> None:
    for ax in [ax_linear, ax_log]:
        for year, df in dfs.items():
            ax.plot(df.index, df[_N_SUBMISSIONS], label=year)
        ax.legend()
        ax.set_title("Number of submissions per day")
        ax.set_xlabel("Day")
    ax_linear.set_ylabel("Submissions")
    ax_log.set_ylabel("Submissions (log-scale)")
    ax_log.set_yscale("log")


def _plot_relative(
    dfs: DfDict, ax_linear: matplotlib.axes.Axes, ax_log: matplotlib.axes.Axes
) -> None:
    for ax in [ax_linear, ax_log]:
        for year, df in dfs.items():
            ax.plot(df.index, df[_Q_SUBMISSIONS], label=year)
        ax.legend()
        ax.set_title("Share of submissions per day relative to first day")
        ax.set_xlabel("Day")
    ax_linear.set_ylabel("Share of submissions")
    ax_log.set_ylabel("Share of submissions (log-scale)")
    ax_log.set_yscale("log")


def _plot(dfs: DfDict) -> None:
    fig, axs = plt.subplots(ncols=2, nrows=2, figsize=(18, 12))
    _plot_absolute(dfs, axs[0][0], axs[1][0])
    _plot_relative(dfs, axs[0][1], axs[1][1])
    filepath = Path(git_root()) / "submissions.png"
    fig.savefig(filepath)
    print(f"Saved file to {filepath}.")


@click.command()
@click.argument("data_dir", type=click.Path(exists=True))
def main_cli(data_dir):
    dfs = _load_data(Path(data_dir))
    _plot(dfs)


if __name__ == "__main__":
    main_cli()
