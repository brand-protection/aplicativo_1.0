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

## MERCADO LIVRE ##
ml_url_base = []
ml_urls = []
ml_price = []
ml_seller = []
ml_installment = []


#### URLS DE PRODUTOS ######
Urls_products = ['https://celulares.mercadolivre.com.br/smartwatches-e-acessorios/huawei/novo/huawei-band-6_NoIndex_True#applied_filter_id%3DITEM_CONDITION%26applied_filter_name%3DCondi%C3%A7%C3%A3o%26applied_filter_order%3D15%26applied_value_id%3D2230284%26applied_value_name%3DNovo%26applied_value_order%3D1%26applied_value_results%3D97%26is_custom%3Dfalse',
                 'https://celulares.mercadolivre.com.br/smartwatches-e-acessorios/huawei/cor-da-pulseira-matte-black/novo/huawei-watch-gt-2_NoIndex_True#applied_filter_id%3DWRISTBAND_COLOR%26applied_filter_name%3DCor+da+pulseira%26applied_filter_order%3D7%26applied_value_id%3D37643%26applied_value_name%3DMatte+black%26applied_value_order%3D10%26applied_value_results%3D27%26is_custom%3Dfalse',
                 'https://celulares.mercadolivre.com.br/smartwatches-e-acessorios/huawei/novo/huawei-watch-fit_NoIndex_True#applied_filter_id%3DITEM_CONDITION%26applied_filter_name%3DCondi%C3%A7%C3%A3o%26applied_filter_order%3D14%26applied_value_id%3D2230284%26applied_value_name%3DNovo%26applied_value_order%3D1%26applied_value_results%3D66%26is_custom%3Dfalse',
                 'https://celulares.mercadolivre.com.br/smartwatches-e-acessorios/huawei/novo/huawei-watch-gt2-pro_NoIndex_True#applied_filter_id%3DITEM_CONDITION%26applied_filter_name%3DCondi%C3%A7%C3%A3o%26applied_filter_order%3D11%26applied_value_id%3D2230284%26applied_value_name%3DNovo%26applied_value_order%3D1%26applied_value_results%3D16%26is_custom%3Dfalse',
                 'https://lista.mercadolivre.com.br/huaweti-freebuds-4i_ITEM*CONDITION_2230284_NoIndex_True#applied_filter_id%3DITEM_CONDITION%26applied_filter_name%3DCondição%26applied_filter_order%3D13%26applied_value_id%3D2230284%26applied_value_name%3DNovo%26applied_value_order%3D1%26applied_value_results%3D107%26is_custom%3Dfalse',
                 'https://informatica.mercadolivre.com.br/conectividade-e-redes-roteadores/novo/roteador-huawei-ws5200_NoIndex_True#applied_filter_id%3DITEM_CONDITION%26applied_filter_name%3DCondi%C3%A7%C3%A3o%26applied_filter_order%3D15%26applied_value_id%3D2230284%26applied_value_name%3DNovo%26applied_value_order%3D1%26applied_value_results%3D66%26is_custom%3Dfalse',
                 'https://informatica.mercadolivre.com.br/conectividade-e-redes-roteadores/novo/roteador-huawei-ws5200_NoIndex_True#applied_filter_id%3DITEM_CONDITION%26applied_filter_name%3DCondi%C3%A7%C3%A3o%26applied_filter_order%3D15%26applied_value_id%3D2230284%26applied_value_name%3DNovo%26applied_value_order%3D1%26applied_value_results%3D66%26is_custom%3Dfalse',
                 'https://informatica.mercadolivre.com.br/conectividade-e-redes-roteadores/novo/roteador-huawei-ax3-dual-core_NoIndex_True#applied_filter_id%3DITEM_CONDITION%26applied_filter_name%3DCondição%26applied_filter_order%3D7%26applied_value_id%3D2230284%26applied_value_name%3DNovo%26applied_value_order%3D1%26applied_value_results%3D26%26is_custom%3Dfalse',
                 'https://informatica.mercadolivre.com.br/conectividade-e-redes-roteadores/novo/roteador-huawei-ax3-quad-core_NoIndex_True#applied_filter_id%3DITEM_CONDITION%26applied_filter_name%3DCondição%26applied_filter_order%3D7%26applied_value_id%3D2230284%26applied_value_name%3DNovo%26applied_value_order%3D1%26applied_value_results%3D59%26is_custom%3Dfalse',]

## FUNÇÕES ##
#Categorização 
def categorizao(a):
    if 'band-6' in a:
        return 'Huawei Band 6'
    elif 'band6' in a:
        return 'Huawei Band 6'
    elif 'huawei-6' in a:
        return 'Huawei Band 6'
    elif 'gt-2-sport' in a:
        return 'Huawei Watch GT 2'
    elif 'gt-2' in a:
        return 'Huawei Watch GT 2'
    elif 'watch-fit' in a:
        return 'Huawei Watch Fit'
    elif 'huawei-fit' in a:
        return 'Huawei Watch Fit'
    elif 'gt2-pro' in a:
        return 'Huawei Watch GT2 Pro'
    elif 'gt-2-pro' in a:
        return 'Huawei Watch GT2 Pro'
    elif 'freebuds-4i' in a:
        return 'Huawei Freebuds 4i'
    elif 'huawei-4i' in a:
        return 'Huawei Freebuds 4i'
    elif 'free-buds-4i' in a:
        return 'Huawei Freebuds 4i'
    elif 'huawei-ws5200' in a:
        return 'Huawei WS5200'
    elif 'ws5200' in a:
        return 'Huawei WS5200'
    elif 'huawei-ax3-dual-core' in a:
        return 'Huawei WS7100'
    elif 'dual-core' in a:
        return 'Huaweu ws7100'
    elif 'huawei-ax3-quad-core' in a:
        return 'Huawei WS7200'
    elif 'ws7200' in a:
        return 'Huawei WS7200'
    elif 'quad-core' in a:
        return 'Huawei WS7200'


def ml_search_links(url):
    #Colocando a variável como global 
    global ml_urls
    
    #Tempo mínimo
    time.sleep(2)

    #Fazendo o response 
    response = urlopen(url)
    html = response.read()

    #Criando o soup 
    bs = BeautifulSoup(html, 'html.parser')

    #Pegando todos os links da página 
    for link in bs.find_all('a', href=True):
        ml_urls.append(link['href'])

    #Fazendo o try para próximas páginas
    try:
        next_page_link = bs.find_all(class_='andes-pagination__arrow-title')[-1].text

        #Vendo se na seta está escrito 'Seguinte'
        if next_page_link == 'Seguinte':
            next_url = bs.find_all(class_='andes-pagination__link ui-search-link')[-1]['href']

            #Realizando o loop da função com o link da próxima página
            ml_search_links(next_url)
    except:
        pass

    #Limpando os links 
    ml_urls = [s for s in ml_urls if 'tracking_id' in s]
    ml_urls = [s for s in ml_urls if 'produto' in s]
    ml_urls = [s for s in ml_urls if 'huawei' in s]
    ml_urls = [s for s in ml_urls if not 'ws318n' in s]
    ml_urls = [s for s in ml_urls if not 'freebuds-3i' in s]
    ml_urls = [s for s in ml_urls if not 'freebuds-3' in s]

    

def ml_search_attributes(url):

    #Tempo
    time.sleep(2)

    #Fazendo o response 
    response = urlopen(url)
    html = response.read()

    #TESTE PRINTANDO URL 
    print(url)

    #Criando o soup
    bs = BeautifulSoup(html, 'html.parser')

    #Buscando o preço 
    try:
        price = bs.find(class_='price-tag-fraction').text
        ml_price.append(price)
    except:
        ml_price.append('Erro')

    #Buscando o installment
    try:
        installment = bs.find(class_='ui-pdp-color--GREEN ui-pdp-size--MEDIUM ui-pdp-family--REGULAR').text
        ml_installment.append(installment)
    except:
        installment = bs.find(class_='ui-pdp-color--BLACK ui-pdp-size--MEDIUM ui-pdp-family--REGULAR').text
        ml_installment.append(installment)

    #Vendedor
    seller_link = bs.find(class_='ui-pdp-media__action ui-box-component__action')['href']

    try:   
        #Entrando na página do vendedor
        response = urlopen(seller_link)
        html = response.read()

        #Criando o soup
        bs = BeautifulSoup(html, 'html.parser')

        #Achando o nome do seller 
        seller_name = bs.find(class_='store-info__name').text

        #Append do nome do seller 
        ml_seller.append(seller_name)
    except:
        ml_seller.append(seller_link)


#Função final 
def ml_final():

    #Criando dataset 
    for url in tqdm(Urls_products):
        ml_search_links(url)

    dataset = pd.DataFrame()

    dataset['Urls'] = ml_urls

    dataset = dataset.drop_duplicates()

    #FPegando os atributos com base nas urls 
    for url in tqdm(dataset['Urls']):
        ml_search_attributes(url)

    #Colocando os valores nas colunas
    dataset['Seller'] = ml_seller
    dataset['Preço'] = ml_price
    dataset['Loja'] = 'MERCADO LIVRE'
    dataset["Installment"] = ml_installment

    #Colocando a coluna de preço em números 
    dataset['Preço'] = dataset['Preço'].str.replace('.','')
    dataset['Preço'] = dataset['Preço'].astype('int64')

    #Arrumando a coluna de installment 
    dataset['Parcela'] = dataset['Installment'].str.partition("x")[0]
    dataset['Parcela'] = dataset['Parcela'].str.extract("(\d+)").astype(int)
    dataset["Installment"] = dataset["Installment"].str.partition("R$")[2]
    dataset["Installment"] = dataset["Installment"].str.replace("sem juros","")

    #Aplicando a categorização no dataset 
    dataset['Item'] = dataset['Urls'].apply(categorizao)

    #Mudando o nome das urls para o nome dos sellers corretos 
    dataset['Seller'] = dataset['Seller'].str.replace("https://perfil.mercadolivre.com.br/HUAWEIOFICIAL?brandId=3562",'HUAWEI LOJA OFICIAL')
    dataset['Seller'] = dataset['Seller'].str.replace("https://perfil.mercadolivre.com.br/MPCEL+MOBILE?brandId=3430",'Mpcel Loja Oficial')
    dataset['Seller'] = dataset['Seller'].str.replace("https://perfil.mercadolivre.com.br/MPCEL+MOBILE?brandId=3562",'MPCEL MOBILE')
    dataset['Seller'] = dataset['Seller'].str.replace("https://perfil.mercadolivre.com.br/ONOFREELETROSERRA?brandId=2156",'Onofre Loja Oficial')
    dataset['Seller'] = dataset['Seller'].str.replace("https://perfil.mercadolivre.com.br/ZOOM_STORE?brandId=3598",'Zoom Store Loja Oficial')

    #Pegando apenas as informações que tem o preço maior que 200
    dataset = dataset[dataset['Preço'] > 200]  

    #Exportando o dataset 
    dataset.to_excel('C:/Users/pedro/Documents/FIVE-C/Huawei/downloads/Mercado_livre_urls.xlsx', index=False)

    


    















