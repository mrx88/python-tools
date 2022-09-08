#!/usr/bin/env python3
import requests
import click
from bs4 import BeautifulSoup
import os
import logging
import datetime


def get_html(url, filename=None, year=None, month=None):
    """Returns HTML content from URL and saves it to
     file if filename is given

    Args:
        url (string): URL of the page
        filename (string, optional): File name. Defaults to None.
        year (string, optional): Year for directory. Defaults to None.
        month (string, optional): Month for directory. Defaults to None.

    Returns:
        _type_: _description_
    """
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

        if filename:
            directory = f"{year}/{month}"
            publish_dir = os.path.join('html/', directory)
            filename = filename.replace("/", "")
            if not os.path.exists(publish_dir):
                os.makedirs(publish_dir)
            backup_file = f"{publish_dir}/{filename}.html"
            logging.info(f"Creating file {backup_file}")
            with open(backup_file, "wb") as f:
                f.write(r.content)
            logging.info(f"Backup complete for {url}")
            f.close()
            return r.content, url
        else:
            return r.content, url
    except requests.exceptions.RequestException as e:
        logging.error(f"Requests error: {e}")
        return None


def get_data(html, url):
    """Parse HTML content using BeautifulSoup

    Args:
        html (list): Html content from get_html function
        url (string): URL of the page
    """
    try:
        # Get page numbers
        soup = BeautifulSoup(html, "html.parser")
        pages = soup.find_all(attrs={"class": "page-numbers"})

        month = url.split("/")[-2]
        year = url.split("/")[-3]

        if pages:
            max_pages = pages[1].text
            logging.debug(f"Max pages: {max_pages}")
        else:
            # If there is only one page
            max_pages = 1
            logging.debug(f"Max pages: {max_pages}")

        # Loop through all pages
        for page in range(1, int(max_pages) + 1):
            # Get HTML from page
            html, url = get_html(f"{url}page/{page}")

            # Parse HTML
            soup = BeautifulSoup(html, "html.parser")
            content = soup.find_all(attrs={"itemprop": "headline"})
            # Get published date
            # published_date = soup.find_all(attrs={"class": "published"})
            # print(published_date)
            for htm in content:
                headline = htm.text
                furl = htm.find("a").get("href")
                print(headline, furl)
                logging.info(f"Headline: {headline} | URL: {furl}")
                get_html(furl, headline, year, month)
    except Exception as e:
        logging.error(f"Error in get_data function: {e}")


@click.command()
@click.option('--site', prompt='Enter URL', help='Enter URL')
@click.option('--year', help='Enter year', type=int)
@click.option('--month', help='Enter month', type=int)
@click.option('--startyear', help='Enter start year', type=int, default=2010)
@click.option('--debug', help='Enable debug logging', is_flag=True)
def main(site, year, month, startyear, debug):
    """Main function
    """
    logging.basicConfig(level=logging.INFO if not debug else logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filename='main.log')
    try:
        if year and month:

            logging.debug(f"Fetching data for: {year}/{month}")
            for date_year in range(year, year+1):
                for date_month in range(month, month+1):
                    content, url = get_html(f"{site}/{date_year}/{date_month}/")
                    get_data(content, url)
        else:
            # get this year
            year = datetime.datetime.now().year
            logging.debug(f"Fetching data from {startyear} to {year}")
            for date_year in range(startyear, year+1):
                for date_month in range(1, 13):
                    content, url = get_html(f"{site}/{date_year}/{date_month}/")
                    get_data(content, url)

    except Exception as e:
        logging.error(f"Error in main function: {e}")


if __name__ == '__main__':
    main()
