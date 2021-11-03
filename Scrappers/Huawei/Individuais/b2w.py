#Importando bibliotecas
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
from urllib.request import HTTPRedirectHandler, urlopen
import json as JSON

header_americanas = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.218'}

## AMERICANAS ## 
Urls_americanas = [] 
Sellers_americanas = []
Price_americanas = []
Title_americanas = []
PP_americanas = []
Sellers_ofertas_americanas = []
Price_ofertas_americanas = []
Urls_ofertas_americanas = []
Title_ofertas_americanas = []
PP_ofertas_americanas = []


##Pegando as urls específicas de cada produto
urls_products = ['https://www.americanas.com.br/busca/huawei-band-6?c_legionRegion=935032&c_macroRegion=SP_CAPITAL&c_mesoRegion=3501&content=huawei+band+6&filter=%7B"id"%3A"wit"%2C"value"%3A"Relógio"%2C"fixed"%3Afalse%7D&oneDayDelivery=true&sortBy=relevance&source=nanook&testab=searchTestAB%3Dnew',
                 'https://www.americanas.com.br/busca/huawei-watch-gt-2-sport?c_legionRegion=935032&c_macroRegion=SP_CAPITAL&c_mesoRegion=3501&content=huawei+watch+GT+2+Sport&filter=%7B"id"%3A"wit"%2C"value"%3A"Relógio"%2C"fixed"%3Afalse%7D&oneDayDelivery=true&sortBy=relevance&source=nanook&testab=searchTestAB%3Dnew',
                 'https://www.americanas.com.br/busca/huawei-watch-fit?c_legionRegion=935032&c_macroRegion=SP_CAPITAL&c_mesoRegion=3501&content=huawei+watch+fit&filter=%7B"id"%3A"wit"%2C"value"%3A"Relógio"%2C"fixed"%3Afalse%7D&oneDayDelivery=true&sortBy=relevance&source=nanook&testab=searchTestAB%3Dnew',
                 'https://www.americanas.com.br/busca/huawei-watch-gt2-pro?c_legionRegion=935032&c_macroRegion=SP_CAPITAL&c_mesoRegion=3501&content=huawei+watch+GT2+Pro&filter=%7B"id"%3A"wit"%2C"value"%3A"Relógio"%2C"fixed"%3Afalse%7D&oneDayDelivery=true&sortBy=relevance&source=nanook&testab=searchTestAB%3Dnew',
                 'https://www.americanas.com.br/busca/hawei-freebuds-4i?c_legionRegion=935032&c_macroRegion=SP_CAPITAL&c_mesoRegion=3501&content=hawei+freebuds+4i&filter=%7B"id"%3A"wit"%2C"value"%3A"Fone+Ouvido"%2C"fixed"%3Afalse%7D&oneDayDelivery=true&sortBy=relevance&source=nanook&testab=searchTestAB%3Dnew',
                 'https://www.americanas.com.br/busca/roteador-huawei-ws5200?rc=Roteador+Huawei+ws5200',
                 'https://www.americanas.com.br/busca/roteador-huawei-ax3-dual-core?rc=Roteador+Huawei+ax3+dual-core',
                 'https://www.americanas.com.br/busca/roteador-huawei-ax3-quad-core?rc=Roteador+Huawei+ax3+quad-core']

# FUNÇÕES 

#Pegando os links da página 
def search_links(url):
    global Urls_americanas

    #Criando o tempo 
    time.sleep(20)

    #Criando o response 
    response = requests.get(url, headers=header_americanas)

    #Criando o html 
    html = response.text

    #Criando o soup 
    bs = BeautifulSoup(html, 'html.parser')

    #Achando os links 
    for link in bs.find_all("a", href=True):
        Urls_americanas.append("https://www.americanas.com.br" + link['href'])

    #Limpando as urls 
    Urls_americanas = [s for s in Urls_americanas if 'produto' in s]

#Pegando os atributos da página 
def search_atributes(url):
    global Sellers_ofertas_americanas
    
    #Criando o tempo 
    time.sleep(60)

    #Criando o response 
    response = requests.get(url, headers=header_americanas)

    #Fazendo a condicional para caso não funcione o requests 
    if response.status_code == 403:
        #Esperando o tempo 
        time.sleep(3000)

        #Tentando novamente 
        response = requests.get(url, headers=header_americanas)

    else:
        pass

    #Fazendo o html 
    html = response.text

    #Criando o soup 
    soup = BeautifulSoup(html, 'html.parser')

    #Pegando o vendedor 
    try:
        seller = soup.find(class_='sold-and-delivered__Link-sc-1hkd1iz-0 gwIJks').text
        Sellers_americanas.append(seller)
    except:
        Sellers_americanas.append('Erro')

    #Pegando o preço 
    try: 
        price = soup.find(class_='src__BestPrice-sc-1jvw02c-5 cBWOIB priceSales').text
        Price_americanas.append(price)
    except:
        Price_americanas.append('Erro')

    #Pegando o título 
    try: 
        title = soup.find(class_='product-title__Title-sc-1hlrxcw-0 jyetLr').text
        Title_americanas.append(title)
    except:
        Title_americanas.append('Erro')

    #Pegando o preço parcelado total 
    try: 
        parcelado = soup.find(class_='src__ListPrice-sc-1jvw02c-2 kXsrBq').text
        PP_americanas.append(parcelado)
    except:
        PP_americanas.append('Erro')

    try:
        #Vendo se tem o texto de mais ofertas 
        soup.find(class_='more-offers__Text-sc-15yqej3-0 bourXY').text
        
        more_offers_link = 'https://www.americanas.com.br' + soup.find(class_='more-offers__Touchable-sc-15yqej3-2 Yhphg')['href']

        #Esperando 10 segundos para entrar na página 
        time.sleep(10)           

        #Fazendo o request no link das ofertas 
        response = requests.get(more_offers_link, headers=header_americanas)
        html = response.text

        #Criando o soup da página com mais ofertas 
        bs = BeautifulSoup(html, 'html.parser')

        #Pegando o nome de todos os sellers menos do primeiro 
        for name in bs.find_all(class_='sold-and-delivery__Seller-sc-1fgd6h1-1 homeqq')[2:]:
            Sellers_ofertas_americanas.append(name.text)

        #Limpando o nome da americanas 
        Sellers_ofertas_americanas = [s for s in Sellers_ofertas_americanas if not 'Americanas' in s]

        #Pegando o preço dos produtos 
        for price in bs.find_all(class_='src__BestPrice-sc-1jvw02c-5 cBWOIB priceSales')[1:]:
            Price_ofertas_americanas.append(price.text)
            Urls_ofertas_americanas.append(url)
            Title_ofertas_americanas.append(title)
            PP_ofertas_americanas.append(price.text)
    except:
        pass

#Função final 
def bw2_final():
    #Criando a variável da página 
    pagina = 0 

    #Fazendo o while das urls 
    while pagina <= 24:

        #Criando a url 
        url_base = 'asdasdsd{}'.format(pagina)

        #Fazendo a função 
        search_links(url_base)

        #Acrescentando a página 
        pagina = pagina + 24 

    #Criando o DataFrame
    Dataset = pd.DataFrame()

    #Colocando as urls 
    Dataset['Urls'] = Urls_americanas

    #Vendo a quantidade 
    Dataset.shape

    #Deletando as duplicadas 
    Dataset = Dataset.drop_duplicates()

    #Fazendo a função com as urls dentro do dataset 
    for url in Dataset['Urls']:
        search_atributes(url)

    #Criando Dataset das ofertas 
    Dataset = pd.DataFrame()

    Dataset["Urls"] = Urls_americanas + Urls_ofertas_americanas
    Dataset['Sellers'] = Sellers_americanas + Sellers_ofertas_americanas
    Dataset['Preço'] = Price_americanas + Price_ofertas_americanas
    Dataset["Título"] = Title_americanas + Title_ofertas_americanas
    Dataset['Preço_parcelado'] = PP_americanas + PP_ofertas_americanas

    #Exportando o dataset 
    Dataset.to_excel("downloads/b2w_urls.xlsx", index=False)
    
    



























