from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from django import forms

import time

def scraping(text):
    url = 'https://opac.lib.u-ryukyu.ac.jp/opc/xc/search/{}'.format(text)
    
    # try:
    options = Options()
    options.add_argument('--headless')
    try:
        driver = webdriver.Chrome(options=options)
    except : raise forms.ValidationError("処理中に問題が発生しました。")

    driver.get(url)
    time.sleep(1)

    current_url = driver.current_url

    is_right_id = False
    cTop = ""
    cMdl = ""
    cBtm = ""

    try:
        if 'opc/recordID/catalog.bib/' in current_url:
            is_right_id = True
            cTop = driver.find_element(By.XPATH, '//li[@class="cTop"]').text
            cMdl = driver.find_element(By.XPATH, '//li[@class="cMdl"]').text
            cBtm = driver.find_element(By.XPATH, '//li[@class="cBtm"]').text
    except:
        raise forms.ValidationError("処理がタイムアウトしました。")

    info = {
        "is_right_id" : is_right_id,
        "cTop" : cTop,
        "cMdl" : cMdl,
        "cBtm" : cBtm
    }
    
    driver.quit()

    return info
