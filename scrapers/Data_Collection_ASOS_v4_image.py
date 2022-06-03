import selenium
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
import urllib.request
from tqdm import tqdm
import csv
import json
from bs4 import BeautifulSoup
import Data_Collection_ASOS_v5
import time

def download_images(self, src: str, i: int) -> None:

        if not os.path.exists('watch_data/images'):
            os.makedirs('watch_data/images')

        try:
            urllib.request.urlretrieve(src, f"watch_data/images/watch_image_{i}.jpg")
        except TypeError:
            pass
        except ContentTooShortError:
            pass
def get_images()
    image_url = self.imagesrc_list[i]
    image_name = f'{self.product_id_num}.jpg'
    urllib.request.urlretrieve(image_url, image_name)
