# Introduction

Simple program to save multiple web page html content as files.


Html files will be saved to local folder under ```html/<year>/<month>``` directory.

Goal was to play with bs4 python library for specific site(s) with specific url(s) and html attributes.

## Prerequisites

We assume the web page URLs are the following:

```
https://<site>/<year number>/<month number>/
```

Python version and dependencies are defined in Pipfile.

## Usage

```
Usage: main.py [OPTIONS]

  Main function

Options:
  --site TEXT          Enter URL
  --year INTEGER       Enter year
  --month INTEGER      Enter month
  --startyear INTEGER  Enter start year
  --debug              Enable debug logging
  --help               Show this message and exit.

pipenv run python main.py --site https://<site> --year <year> --month <month>
pipenv run python main.py --site https://<site> --year 2022 --month 9
```

## Logs

Logs are visibile in main.log file under local directory.