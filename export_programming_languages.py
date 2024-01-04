import json
from collections import Counter
from functools import cache
from pathlib import Path

import click
import requests
from dotenv import dotenv_values


def _gh_pat() -> str:
    pat = dotenv_values(".env")["GITHUB_PAT"]
    if not pat:
        raise ValueError()
    return pat


@cache
def _headers():
    return {"Authorization": f"token {_gh_pat()}"}


def _repos(n_pages: int = 2) -> list[tuple[str, str]]:
    lookup = []
    for page in range(n_pages):
        response = requests.get(
            f"https://api.github.com/search/repositories?q=adventofcode&per_page=100&page={page}",
            headers=_headers(),
        )

        try:
            for item in response.json()["items"]:
                owner = item["owner"]["login"]
                repo = item["name"]
                lookup.append((owner, repo))
        except:
            print(f"broke at {page}")
            break

        lookup = list(set(lookup))
        return lookup


def _determine_language(owner: str, repo: str) -> str | None:
    response = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/languages", headers=_headers()
    )
    data = json.loads(response.text)

    # We know that the most used language always comes first.
    try:
        return next(iter(data))
    except:
        return None


def _export(
    languages: Counter, data_dir: Path, filename: str = "languages.json"
) -> None:
    filepath = data_dir / filename
    with open(filepath, "w") as filehandle:
        json.dump(languages, filehandle)
    print(f"Exported programming language file to {filepath}.")


@click.command()
@click.argument("data_dir", type=click.Path(exists=True))
def main_cli(data_dir):
    repos = _repos()
    languages = Counter()
    for owner, repo in repos:
        language = _determine_language(owner, repo)
        if language:
            languages[language] += 1
    _export(languages, Path(data_dir))


if __name__ == "__main__":
    main_cli()
