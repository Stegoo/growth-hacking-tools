#Follow People on Twitter

A small script to follow a list of people on twitter coming from tools such as X or Y.

## Requirements

* Python3
* pip

Run `pip install git+https://github.com/bear/python-twitter --upgrade`

##Config

Set your username and twitter's api key in the config.cfg file (tuto here : https://python-twitter.readthedocs.org/en/latest/getting_started.html)

##Format of the csv file

Specifiy one account name per line (see the example file).

## Usage

`python twitter-follow-people.py file` where file is your csv file (1 account to follow per line)
