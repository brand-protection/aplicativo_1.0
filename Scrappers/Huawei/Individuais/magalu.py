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

header_magazine = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}


## MAGAZINE LUIZA ##
magazine_urls = []
magazine_sellers = []
magazine_price = []
magazine_installments = []
magazine_proxies = {'http':"187.92.71.154"}
url_base = 'https://www.magazineluiza.com.br'

#Teste de lista 
lista_teste = []

#Definindo as urls para cada produto
urls_produtos = ['https://www.magazineluiza.com.br/busca/huawei+band+6/?filters=brand---huawei',
                 'https://www.magazineluiza.com.br/busca/huawei+watch+GT+2+Sport/',
                 'https://www.magazineluiza.com.br/busca/huawei+watch+fit/',
                 'https://www.magazineluiza.com.br/busca/huawei+watch+GT+2+pro/',
                 'https://www.magazineluiza.com.br/busca/huawei+freebuds+4i/',
                 'https://www.magazineluiza.com.br/busca/roteador+huawei+ws5200/',
                 'https://www.magazineluiza.com.br/busca/roteador+huawei+ax3+dual-core/',
                 'https://www.magazineluiza.com.br/busca/roteador+huawei+ax3+quad-core/']

def search_links(url):
    #Passando a variável global 
    global magazine_urls
    
    #Criando o tempo 
    time.sleep(100)

    #Fazendo o requests 
    driver = webdriver.Chrome(executable_path=r'C:\Users\kcava\OneDrive\Documentos\FIVE C\aplicativo_1.0\Dados\Selenium\chromedriver_94.exe')
    
    #Abrimdo a página 
    driver.get(url)

    #Tempo para carregar a página 
    time.sleep(2)

    #Lendo o html da página de origem 
    bs = BeautifulSoup(driver.page_source, 'html.parser')

    #Achando todos os links 
    for link in bs.find_all("a", href=True):
        magazine_urls.append('https://www.magazineluiza.com.br' + link['href'])

    #Limpando todos os links
    magazine_urls = [s for s in magazine_urls if '/p/' in s]

    #Fechando o driver
    driver.close()

def search_attributes(url):
    #Tempo 
    time.sleep(100)

    #Fazendo o requests 
    driver = webdriver.Chrome(executable_path=r'C:\Users\kcava\OneDrive\Documentos\FIVE C\aplicativo_1.0\Dados\Selenium\chromedriver_94.exe')
    
    #Abrimdo a página 
    driver.get(url)

    #Tempo para carregar a página 
    time.sleep(2)

    #Lendo o html da página de origem 
    bs = BeautifulSoup(driver.page_source, 'html.parser')
 
    #try do preço 
    try: 
        price = bs.find(class_='price-template__text').text
        magazine_price.append(price)
    except:
        magazine_price.append("Preço indisponível")

    #Fazendo o try do seller 
    try: 
        seller = bs.find(class_="seller-info-button js-seller-modal-button").text
        magazine_sellers.append(seller)
    except:
        magazine_sellers.append("Erro")

    #Fazendo o try do preço
    lista = [] 
    try:
        for ultag in bs.find_all('ul', {'class':'method-payment__values--general-cards'}):
            for litag in ultag.find_all('li'):
                lista.append(litag.text)

        magazine_installments.append(lista[-1])
    except:
        magazine_installments.append("0")

    #Fechando o driver
    driver.close()

#final 
def magazine_final():

    #Fazendo a primeira função 
    for url in tqdm(urls_produtos):
        search_links(url)

    #Pegando os atributos 
    for url in tqdm(magazine_urls):
        search_attributes(url)

    #Criando o DataFrame 
    Dataset_magalu = pd.DataFrame()

    #Colocando os resultados na coluna
    Dataset_magalu['Urls'] = magazine_urls
    Dataset_magalu["Sellers"] = magazine_sellers
    Dataset_magalu["Preço"] = magazine_price
    Dataset_magalu["Loja"] = 'MAGAZINE LUIZA'
    Dataset_magalu["Installment"] = magazine_installments
    Dataset_magalu['Parcelas'] = Dataset_magalu['Installment'].str.partition("x")[0]
    Dataset_magalu['Parcelas'] = Dataset_magalu['Parcelas'].str.replace(" ","")
    Dataset_magalu["Installment"] = Dataset_magalu['Installment'].str.partition("$")[2]
    Dataset_magalu["Installment"] = Dataset_magalu["Installment"].str.replace("sem juros","")
    Dataset_magalu["Installment"] = Dataset_magalu["Installment"].str.replace(" ","")
    
    #Fazendo a limpeza de espaços dentro dos sellers 
    Dataset_magalu['Sellers'] = Dataset_magalu['Sellers'].str.replace(" ","",1)

    #Exportando os dados 
    Dataset_magalu.to_excel("C:/Users/kcava/OneDrive/Documentos/FIVE C/aplicativo_1.0/Scrappers/Huawei/Downloads/magazine_urls.xlsx", index=False)







