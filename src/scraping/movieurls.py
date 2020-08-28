import json
import time
import itertools  

from bs4 import BeautifulSoup
import requests
import pandas as pd

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from tqdm import tqdm_notebook

def extract_movie_urls_from_page():
     a_list = driver.find_elements_by_xpath('//a[@class="title"]')
     urls = [a.get_attribute('href') for a in a_list]
     dedup_urls = list(set(urls))
     return dedup_urls
 
def go_next_page():
    try:
        button = driver.find_element_by_xpath('//a[@rel="next"]')
        return True, button
    except NoSuchElementException:
        return False, None
    
genres = ['action', 'adventure', 'animation', 'biography', 'comedy', 'crime', 'documentary',
          'drama', 'family', 'fantasy', 'film-noir', 'history', 'horror', 'music', 'musical',
          'mystery', 'news', 'reality-tv', 'romance', 'sci-fi', 'short', 'sport', 'thriller',
          'war', 'western']

test_genre = ['action']
    
base_url = 'https://www.metacritic.com/browse/movies/genre/name'

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")
 
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
 
driver = webdriver.Chrome(options=options)
 
timeout = 3

driver.get(base_url)
data = list(test_genre)

movie_urls = []
movie_genres = []
temp_urls = []
for genre in tqdm_notebook(data):
        url = base_url + '/' + genre + '?view=condensed'
        driver.get(url)
        try: 
            element_present = EC.presence_of_element_located(
                    (By.CLASS_NAME, 'title'))
             
            WebDriverWait(driver, timeout).until(element_present)
        except:
            pass
         
        next_page = True
        c = 0
        while next_page:
            extracted_movie_urls = extract_movie_urls_from_page()
            movie_urls += extracted_movie_urls
            temp_urls += extracted_movie_urls
            for movie in temp_urls:
                movie_genres.append(genre)
            temp_urls.clear()
            next_page, button = go_next_page()
            
            if next_page:
                c += 1
                print(c)
                print(genre)
                next_url = url + f'&page={c}'
                driver.get(next_url)
                try: 
                    element_present = EC.presence_of_element_located(
                            (By.CLASS_NAME, 'title'))
                     
                    WebDriverWait(driver, timeout).until(element_present)
                except:
                    pass

consolidated_data = {movie_urls[i]: movie_genres[i] for i in range(len(movie_urls))}
df_consolidate_data = pd.DataFrame(consolidated_data.items(), columns=['Movie Urls', 'Genres'])
with open(r'C:\Users\Ryan\Downloads\movie_urls_action.csv', 'a', ) as f:
    df_consolidate_data.to_csv(f, mode='a', header=f.tell()==0, index=False, line_terminator='\n')
print('Done')