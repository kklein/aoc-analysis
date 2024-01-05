#!/bin/bash

for year in "2020" "2021" "2022" "2023"
do
    urls=$(curl https://adventofcode.com/$year/leaderboard | grep -o 'https://github.com/[^"]*')

    echo $urls

    for url in $urls
    do
	user=$(echo $url | sed -n 's|https://github.com/||p')
	# Curl the url and extract the required information
	location=$(curl -s $url | grep -o 'aria-label="Home location: [^"]*' | sed -n 's|aria-label="Home location: ||p')
	# Write the output to a separate file
	echo $location > "data/locations/${user//\//-}".txt
    done
done
