#Importando as bibliotecas 
import pandas as pd 
import requests 
import time
from requests.models import Response 
from requests_html import HTML
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import WebDriverException
from tqdm import tqdm
from urllib.request import urlopen
import json as JSON

## EXTRA ##
extra_urls = []
extra_sellers = []
extra_price = []
extra_installments = []
extra_sellers_ofertas = []
extra_price_ofertas = []
extra_urls_ofertas = []
extra_installments_ofertas = []


#Urls dos produtos 
urls_products = ['https://www.extra.com.br/huawei-band-6/b',
                 'https://www.extra.com.br/huawei-watch-gt-2-sport-matte-black/b',
                 'https://www.extra.com.br/huawei-fit/b?sortby=descprice',
                 'https://www.extra.com.br/huawei-watch-gt2-pro/b',
                 'https://www.extra.com.br/huawei-freebuds-4i/b',
                 'https://www.extra.com.br/roteador-huawei-ws5200/b',
                 'https://www.extra.com.br/roteador-huawei-ax3-dual-core/b',
                 'https://www.extra.com.br/roteador-huawei-ax3-quad-core/b']

## extra ## 
def extra_search_urls(url):
    #Colocando a variável como global 
    global extra_urls

    #Inicializando webdriver 
    driver = webdriver.Chrome(executable_path=r'C:\Users\pedro\Documents\FIVE-C\Aplicativo\project\Dados\Selenium\chromedriver_95.exe')

    #Inicializando o driver na página 
    driver.get(url)

    #Criando o beautiful usando o driver 
    bs = BeautifulSoup(driver.page_source, 'html.parser')

    #Fechando o driver
    driver.close()

    #Pegando os links 
    for link in bs.find_all("a"):
        extra_urls.append(link['href'])

    #Limpando os links para apenas produtos 
    extra_urls = [s for s in extra_urls if 'IdSku=' in s]


def extra_search_attributes(url):
    #Criando o webdriver 
    driver = webdriver.Chrome(executable_path=r'C:\Users\pedro\Documents\FIVE-C\Aplicativo\project\Dados\Selenium\chromedriver_94.exe')
    driver.get(url)

    #Tempo 
    time.sleep(3)

    #Fazendo o soup 
    bs = BeautifulSoup(driver.page_source, 'html.parser')

    #Fechandoo chrome
    driver.close()

    #Fazendo o try do seller 
    try:
        extra_sellers.append(bs.find(class_='text-primary css-fv6pw7 eym5xli0').text)
    except:
        extra_sellers.append("Erro")

    #Fazendo o try do preço 
    try:
        extra_price.append(bs.find(class_='product-price-value').text)
    except:
        extra_price.append("Erro")

    #Fazendo o try para pegar o preço installment
    try:
        installment = bs.find(class_="product-price-max").text
        extra_installments.append(installment)
    except:
        extra_installments.append(0)

    #Vendo se tem mais ofertas do mesmo produto 
    try:
        ofertas = bs.find_all(class_='css-ysnrax eym5xli0')
        for seller_name in ofertas:
            extra_sellers_ofertas.append(seller_name.text)
            extra_urls_ofertas.append(url)
            extra_installments_ofertas.append(bs.find(class_="product-price-max").text)
    except:
        pass

    # #Fazendo o try para pegar o preço 
    # try:
    #     another_price = bs.find_all(class_='prod-sellers__seller-price css-11oup1l eym5xli0')
    #     for item in another_price:
    #         extra_price_ofertas.append(item.text)
    # except:
    #     extra_price_ofertas.append("ERRO")


def final_via_varejo():

    for url in urls_products:
        #Fazendo extra função base 
        extra_search_urls(url)

    #Fazendo a função para cada url de produto 
    for url in tqdm(extra_urls):
        extra_search_attributes(url)

    #Criando o dataset 
    dataset_extra = pd.DataFrame()

    #Colocando as informações dentro do dataframe 
    dataset_extra['Urls'] = extra_urls #+ extra_urls_ofertas
    dataset_extra['Seller'] = extra_sellers #+ extra_sellers_ofertas
    dataset_extra['Price'] = extra_price #+ extra_price_ofertas
    dataset_extra['Installment'] = extra_installments #+ extra_installments_ofertas

    #Arrumando a coluna de valores installmnet
    dataset_extra['Parcela'] = dataset_extra['Installment'].str.partition("x")[0]
    dataset_extra['Installment'] = dataset_extra['Installment'].str.partition("$")[2]

    #Item
    #dataset_extra['Item'] = dataset_extra['Urls'].apply(limpeza)

    #Exportando 
    dataset_extra.to_excel(r"C:\Users\pedro\Documents\FIVE-C\Huawei\downloads\extra.xlsx", index=False)







