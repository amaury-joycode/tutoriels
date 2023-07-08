import os
import re
import time

from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox import options as firefox_options


def get_pages(count=1, headless=False):
    """Fetch a specific count of result pages of property advertisements

    Args:
        count (int, optional): Number of result pages to fetch. Defaults to 1.
        headless (bool, optional): Whether to hide the browser. Defaults to False.

    Returns:
        list: pages HTML as utf-8 encoded bytes
    """

    pages = []

    driver = get_driver(headless=headless)

    for page_nb in range(1, count + 1):
        page_url = f"https://www.logic-immo.com/appartement-paris/location-appartement-paris-75-100_1-{page_nb}.html"
        driver.get(page_url)
        if page_nb == 1:
            time.sleep(15)
        else:
            time.sleep(10)
        pages.append(driver.page_source.encode("utf-8"))
    return pages


def get_driver(headless=False):
    """Returns a selenium firefox webdriver

    Args:
        headless (bool, optional): Whether to hide the browser. Defaults to False.

    Returns:
        selenium.webdriver.Firefox: firefox webdriver
    """
    if headless:
        options = firefox_options.Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
    else:
        driver = webdriver.Firefox()
    return driver


def save_pages(pages):
    """Saves HTML pages into the "data" folder

    Args:
        pages (list): list of pages as bytes
    """
    os.makedirs("data", exist_ok=True)
    for page_nb, page in enumerate(pages):
        with open(f"data/page_{page_nb}.html", "wb") as f_out:
            f_out.write(page)


def parse_pages():
    """Parse all pages from the data folder

    Returns:
        pd.DataFrame: parsed data
    """
    results = pd.DataFrame()
    pages_paths = os.listdir("data")
    for pages_path in pages_paths:
        with open(os.path.join("data", pages_path), "rb") as f_in:
            page = f_in.read().decode("utf-8")
            results = results.append(parse_page(page))
    return results


def parse_page(page):
    """Parses data from a HTML page and return it as a dataframe

    The parsed data for each property advertisement is :
    - loyer (€) (rent)
    - type
    - surface (m²) (area)
    - nb_pieces (room number)
    - emplacement (location)
    - description

    Args:
        page (bytes): utf-8 encoded HTML page

    Returns:
        pd.DataFrame: Parsed data
    """
    soup = BeautifulSoup(page, "html.parser")
    result = pd.DataFrame()

    result["loyer (€)"] = [
        clean_price(tag) for tag in soup.find_all(attrs={"class": "announceDtlPrice"})
    ]
    result["type"] = [
        clean_type(tag) for tag in soup.find_all(attrs={"class": "announceDtlInfosPropertyType"})
    ]
    result["surface (m²)"] = [
        clean_surface(tag)
        for tag in soup.find_all(attrs={"class": "announceDtlInfos announceDtlInfosArea"})
    ]
    result["nb_pieces"] = [
        clean_rooms(tag)
        for tag in soup.find_all(attrs={"class": "announceDtlInfos announceDtlInfosNbRooms"})
    ]
    result["emplacement"] = [
        clean_postal_code(tag) for tag in soup.find_all(attrs={"class": "announcePropertyLocation"})
    ]
    result["description"] = [
        tag.text.strip() for tag in soup.find_all(attrs={"class": "announceDtlDescription"})
    ]

    return result


def clean_price(tag):
    text = tag.text.strip()
    price = int(text.replace("€", "").replace(" ", ""))
    return price


def clean_type(tag):
    text = tag.text.strip()
    return text.replace("Location ", "")


def clean_surface(tag):
    text = tag.text.strip()
    return int(text.replace("m²", ""))


def clean_rooms(tag):
    text = tag.text.strip()
    rooms = int(text.replace("p.", "").replace(" ", ""))
    return rooms


def clean_postal_code(tag):
    text = tag.text.strip()
    match = re.match(".*\(([0-9]+)\).*", text)
    return match.groups()[0]


def main():
    pages = get_pages(count=20)
    save_pages(pages)


if __name__ == "__main__":
    main()
