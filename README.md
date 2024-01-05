

1. Get a [GitHub Personal Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
   and a [Google Maps API key](https://developers.google.com/maps/get-started#create-project). Add
   add them to an `.env` file as such:
   ```
   GOOGLE_API_KEY=YOUR_API_KEY
   GITHUB_PAT=YOUR_GITHUB_PAT
   ```
2. Build the conda environment by running `$ conda env create -f environment.yml`.
3. Activate the conda environment by running `$ conda activate aoc-analysis`.
4. Export the location data by running `$ ./export_locations.sh`
5. Generate the location plots by running `$ python plot_locations.py data/locations`
6. Export the programming language data by running `$ python export_programming_languages.py data`
7. Generate the programming language plots by running `$ python plot_programming_languages.py data`.
