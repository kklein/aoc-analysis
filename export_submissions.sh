#!/bin/bash

for year in "2021" "2022" "2023"
do
    echo $year
    # Create a header in csv file.
    echo "day,n_submissions" >> data/submissions/$year.csv

    entire_html=$(curl https://adventofcode.com/$year/stats)
    days=$(echo $entire_html | grep -o "href=\"/${year}/day/[^\"]*" | sed -n "s|href=\"/${year}/day/||p")

    for day in $days
    do
	submissions=$(echo $entire_html | grep -o "> *${day} <span class=\"stats-both\">[^<]*" | sed -n "s|> *${day} <span class=\"stats-both\">||p")
	echo "$day,$submissions" >> data/submissions/$year.csv
    done
done
