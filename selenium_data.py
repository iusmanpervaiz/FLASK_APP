from selenium import webdriver
from selenium.webdriver.common.by import By
from scraping import productDataScrape
import time

def driverFunc(prod_data):
    url = "https://www.weboc.gov.pk/(S(pumllbvg3fubum4pgvf1wou0))/DownloadValuationData.aspx"
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(executable_path = "C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe", options=options)
    driver.get(url)
    time.sleep(3)
    driver.find_element(By.XPATH,'//*[@name="txtDescription"]').send_keys(prod_data)
    driver.find_element(By.XPATH,'//*[@name="btnSearch"]').click()
    time.sleep(3)
    html = driver.page_source
    data= productDataScrape(html)
    driver.close()
    return data

