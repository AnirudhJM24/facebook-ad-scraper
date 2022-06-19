import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import sys


def scroll_to_bottom(driver):
    old_position = 0
    new_position = None

    while new_position != old_position:
        # Get old scroll position
        old_position = driver.execute_script(
            ("return (window.pageYOffset !== undefined) ?"
             " window.pageYOffset : (document.documentElement ||"
             " document.body.parentNode || document.body);"))
        # Sleep and Scroll
        time.sleep(1)
        driver.execute_script((
            "var scrollingElement = (document.scrollingElement ||"
            " document.body);scrollingElement.scrollTop ="
            " scrollingElement.scrollHeight;"))
        # Get new position
        new_position = driver.execute_script(
            ("return (window.pageYOffset !== undefined) ?"
             " window.pageYOffset : (document.documentElement ||"
             " document.body.parentNode || document.body);"))


def main():
    exe_path = 'chromedrive/chromedriver'
    driver = webdriver.Chrome(exe_path)
    driver.get(sys.argv[2])
    print(driver.title)
    driver.implicitly_wait(0)

    for i in range(0, 10):
        #print(i)
        scroll_to_bottom(driver)

    search = driver.find_elements(
        By.XPATH, '//div[@class="_7jyg _7jyh"]'
    )
    primarytext = []
    header2 = []
    header3 = []
    creativelinks = []
    CTA = []

    print(len(search))
    for i in search:
        # time.sleep(2)
        try:

            primary_text = i.find_element(By.XPATH, './/div[@class="_7jyr _a25-" or @class = "_7jyr"]')
            #print(primary_text.text)
            primarytext.append(primary_text.text)

        except NoSuchElementException:
            primarytext.append(None)
            # continue
        try:

            header_2 = i.find_element(By.XPATH, './/div[@class="_8jh2"]')
            header2.append(header_2.text)
            #print(header_2.text)
        except NoSuchElementException:
            #print('no header 2')
            header2.append(None)
            # continue
        try:

            header_3 = i.find_element(By.XPATH, './/div[@class="_8jh3"]')
            header3.append(header_3.text)
            #print(header_3.text)
        except NoSuchElementException:
            #print('no header 3')
            header3.append(None)
            # continue
        try:
            image = i.find_element(By.XPATH, './/img[@class="_7jys img"]')
            creativelinks.append(image.get_attribute("src"))
        except NoSuchElementException:
            creativelinks.append(None)
            # continue
        try:

            callta = i.find_element(By.XPATH, './/div[@class="_8jh0"]')
            CTA.append(callta.text)
            #print(callta.text)
        except NoSuchElementException:
            #print('no cta')
            CTA.append(None)
            # continue

    df = pd.DataFrame()
    df['primarytext'] = primarytext
    df['header2'] = header2
    df['header3'] = header3
    df['img links'] = creativelinks
    df['cta'] = CTA

    df.to_csv( 'scraped_data/'+ sys.argv[1] + 'scraped_data.csv', index=False)

if __name__ == '__main__':
    main()

