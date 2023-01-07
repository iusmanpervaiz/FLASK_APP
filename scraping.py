from bs4 import BeautifulSoup
from selenium_data import *

def productDataScrape(html):
    soup = BeautifulSoup(html,'lxml')
    products_data_list = []
    p_data = soup.find_all('td',{'style' : 'width:70px;'})
    for i in p_data:
        if i and i is not None:
            i = i.text.strip()
            product_description, product_value = i.split('\n\n')[0],i.split('\n\n')[1]
            product_hs_code, product_unit_value = product_value.split(',')[0],product_value.split(',')[1]
            product_unit_value = product_unit_value.split('Unit Value  ')[1]
            product_hs_code = product_hs_code.split(': ')[1].strip()
        Data = {
            "Product Description" : product_description,
            "Product HS Code" : product_hs_code,
            "Product Value" : product_unit_value
            }
        products_data_list.append(Data)

    return products_data_list,Data

# productDataScrape("phones")