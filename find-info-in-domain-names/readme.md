# Find info in domain names

This script is able to search articles mentioning a given term through a list of websites. It fetches the author and language of every articles mentioning the term.

## Requirements

* Python3

## Config

Set your api key and cse id in the `config.cfg` file

To get a cse id, create a [search engine](https://cse.google.com/cse/all) and set it to [search the entire web] (https://support.google.com/customsearch/answer/2631040?hl=en)

To get your api key, create a custom [search api key](https://console.developers.google.com)

## Usage

First parameter is the input file containing all the urls (one per line).
Second parameter is the output file that the program is going to fill (may not exist on your disk yet).
Third parameter is the term you are looking for.

Example: `python find_info_in_domain_names.py site_list_example.csv site_list_output_example.csv qwant`

## Format of the csv file

Specifiy one domain per line (see the example file).

## Format of each line of the outpout csv file

base_url;term_has_been_mentionned;url;author;language

Example:
`miss-seo-girl.com;Yes;http://www.miss-seo-girl.com/quelle-est-linfluence-reelle-des-reseaux-sociaux-sur-le-seo/;Alexandra Martin;fr`
