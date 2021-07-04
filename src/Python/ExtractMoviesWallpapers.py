from ExtractDataFromCsv import *
from selenium import webdriver
import time
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

NOT_FOUND_ELEMENT = 'N/A'


def connect_to_the_browser():
    options = Options()
    options.headless = True
    global browser
    browser = webdriver.Chrome(
        executable_path=r"C:\Users\DELL\Desktop\Python\pycharm files - backup\ChromeDriver\chromedriver.exe",
        options=options)
    browser.get("https://wall.alphacoders.com/by_collection.php?id=175")
    time.sleep(3)


def wallpaper_scraper():
    connect_to_the_browser()
    movies_wallpaper_dict = {}
    for movie in read_movies_file('movie list.csv'):
        movie_search(movie)

        try:
            print('open movie website')
            movie_wallpaper_link = browser.find_element_by_css_selector(
                'div.thumb-container-big> div.thumb-container > div.boxgrid > a').get_attribute('href')
            time.sleep(2)
            browser.get(movie_wallpaper_link)
            time.sleep(2)
            movie_wallpaper = browser.find_element_by_css_selector(
                '#page_container > div.center.img-container-desktop > a > picture > img').get_attribute('src')
        except NoSuchElementException:
            print('no movie wallpaper link found')
            movie_wallpaper = NOT_FOUND_ELEMENT
        movies_wallpaper_dict[movie] = [movie_wallpaper]
    create_csv_file_movie_wallpaper(movies_wallpaper_dict)


def movie_search(movie):
    search_key = browser.find_element_by_css_selector('#search')
    search_key.send_keys(movie)
    search_button = browser.find_element_by_css_selector(
        'body > nav > div.collapse.navbar-collapse.navbar-ex1-collapse > form > div > span > button')
    search_button.click()
    time.sleep(1)


def create_csv_file_movie_wallpaper(movies_data_dict):
    movies_df = pd.DataFrame.from_dict(movies_data_dict, orient='index', columns=['movie wallpaper'])
    movies_df.to_csv('moviesListWallpaper.csv')


if __name__ == '__main__':
    wallpaper_scraper()
