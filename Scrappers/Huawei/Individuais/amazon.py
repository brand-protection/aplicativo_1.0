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
from tqdm import tqdm


#Congiruando o driver 
options = Options()
options.add_argument("--headless")
options.add_argument('--log-level=3')
options.add_argument('--disable-gpu')

#Configurando o driver 
driver = webdriver.Chrome(executable_path=r'C:\Users\kcava\OneDrive\Documentos\FIVE C\aplicativo_1.0\Dados\Selenium\chromedriver_95.exe',options=options)

#Criando as listas 
Urls_amazon = []
Urls_amazon_more = []
Amazon_price = []
Amazon_seller = []
Amazon_title = []
Amazon_installment_price_full = []
Amazon_seller_more = []
Amazon_price_more = []
Amazon_title_more = []

urls_dos_produtos = ['https://www.amazon.com.br/s?k=huawei+band+6&i=electronics&rh=n%3A16209062011%2Cp_89%3AHUAWEI%2Cp_n_condition-type%3A13862762011&dc&qid=1633627909&rnid=13862761011&ref=sr_nr_p_n_condition-type_1',
                     'https://www.amazon.com.br/s?k=huawei+watch+gt2+sport&i=electronics&rh=n%3A16209062011%2Cp_89%3AHUAWEI%2Cp_n_condition-type%3A13862762011&dc&__mk_pt_BR=ÅMÅŽÕÑ&qid=1633627989&rnid=13862761011&ref=sr_nr_p_n_condition-type_1',
                     'https://www.amazon.com.br/s?k=huawei+watch+fit&i=electronics&rh=n%3A16209062011%2Cp_89%3AHUAWEI%2Cp_n_condition-type%3A13862762011&dc&__mk_pt_BR=ÅMÅŽÕÑ&qid=1633628007&rnid=13862761011&ref=sr_nr_p_n_condition-type_1',
                     'https://www.amazon.com.br/s?k=huawei+watch+gt2+pro&i=electronics&rh=n%3A16209062011%2Cp_89%3AHUAWEI%2Cp_n_condition-type%3A13862762011&dc&qid=1633628024&rnid=13862761011&ref=sr_nr_p_n_condition-type_1',
                     'https://www.amazon.com.br/s?k=huawei+freebuds+4i&i=electronics&rh=n%3A16209062011%2Cp_89%3AHUAWEI%2Cp_n_condition-type%3A13862762011&dc&__mk_pt_BR=ÅMÅŽÕÑ&qid=1633628057&rnid=13862761011&ref=sr_nr_p_n_condition-type_1',
                     'https://www.amazon.com.br/s?k=Roteador+Huawei+ws5200&i=electronics&rh=n%3A16209062011%2Cp_89%3AHUAWEI%2Cp_n_condition-type%3A13862762011&dc&__mk_pt_BR=ÅMÅŽÕÑ&qid=1633628077&rnid=13862761011&ref=sr_nr_p_n_condition-type_1',
                     'https://www.amazon.com.br/s?k=Roteador+Huawei+AX3&i=electronics&rh=p_n_condition-type%3A13862762011&dc&__mk_pt_BR=ÅMÅŽÕÑ&qid=1633628100&rnid=13862761011&ref=sr_nr_p_n_condition-type_1',
                     'https://www.amazon.com.br/s?k=roteador+huawei+ax3+quad-core&i=electronics&__mk_pt_BR=ÅMÅŽÕÑ&ref=nb_sb_noss_2']


### FUNÇÕES ###
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


def search_urls():

    #Criando a variável das páginas 
    paginas = 1 

    #Criando o while para pesquisar 
    while paginas <= 2:
        url_base = 'https://www.amazon.com.br/s?k=huawei&page={}&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91'.format(paginas)

        #Realizando a função para pegar os links 
        search_links(url_base)

        #Adicionando o valor para as variáveis 
        paginas = paginas + 1 

#Função para pegar todos os links dentro de uma página 
def search_links(url):
    global Urls_amazon

    #Criando o tempo de rest 
    time.sleep(5)

    #Criando o requests e fazendo o BS
    driver.get(url)
    body_el = driver.find_element_by_css_selector('body')
    html_str = body_el.get_attribute('innerHTML')
    html_obj = HTML(html=html_str)

    #Pegando todos os links 
    Links = [x for x in html_obj.links]

    #Criando os links de produtos 
    products_links = [f'https://www.amazon.com.br{x}' for x in Links]

    #Criando o append para as urls 
    for link in products_links:
        Urls_amazon.append(link)

    Urls_amazon = [s for s in Urls_amazon if '/dp/' in s]
    Urls_amazon = [s for s in Urls_amazon if not '#customerReviews' in s]

#Função para pegar os atributos dentro da página do anúncio
def search_attributes(url):
    global Amazon_seller_more

    #Tempo de espera 
    time.sleep(10)

    #Criando o requests e o BS 
    driver.get(url)
    body_el = driver.find_element_by_css_selector('body')
    html_str = body_el.get_attribute('innerHTML')

    #Criando o soup 
    soup = BeautifulSoup(html_str, 'html.parser')

    #Fazendo o try do nome do vendedor 
    try:
        seller = soup.find(id='sellerProfileTriggerId').text
        Amazon_seller.append(seller)
    except:
        Amazon_seller.append("Erro")

    #Fazendo o try do preço do produto a vista 
    try:
        price = soup.find(id="price_inside_buybox").text
        Amazon_price.append(price)
    except:
        Amazon_price.append("Erro")    

    #Pegando o título do produto 
    try:
        title = soup.find(id='productTitle').text
        Amazon_title.append(title)
    except:
        Amazon_title.append('Erro')

    #Fazendo o try para pegar o preço da parcela 
    try:
        installment = soup.find(class_='best-offer-name a-text-bold').text
        Amazon_installment_price_full.append(installment)
    except:
        Amazon_installment_price_full.append("0")

    #Fazendo o try para ver se tem mais ofertas 
    try:
        soup.find(class_='olp-text-box').text

        #Pegando o texto do número de ofertas 
        ofertas = soup.find(class_='olp-text-box').text

        #Pegando apenas o número em parenteses dentro da frase 
        ofertas = ofertas[ofertas.index("(") + 1:ofertas.rindex(")")]

        #Transformando o número em um integer 
        ofertas = int(ofertas)

        #Fazendo o link de mais ofertas do mesmo produto 
        more_offers = 'https://www.amazon.com.br' + soup.find(class_='a-touch-link a-box olp-touch-link')['href']

        #Tempo de espera 
        time.sleep(3)

        #Fazendo o requests com o link de mais ofertas 
        driver.get(more_offers)
        time.sleep(2)
        body_el = driver.find_element_by_css_selector('body')
        html_str = body_el.get_attribute('innerHTML')

        #Criando o soup
        soup = BeautifulSoup(html_str, 'html.parser')

        #Pegando o nome dos sellers 
        for seller in soup.find_all(class_='a-size-small a-link-normal')[3:]:
            Amazon_seller_more.append(seller.text)

        #Limpando o nome dos sellers 
        Amazon_seller_more = [s for s in Amazon_seller_more if not 'política' in s]
        Amazon_seller_more = [s for s in Amazon_seller_more if not '+' in s]
        Amazon_seller_more = [s for s in Amazon_seller_more if not 'Detalhes' in s]
        Amazon_seller_more = [s for s in Amazon_seller_more if not 'Apagar' in s]
        Amazon_seller_more = [s for s in Amazon_seller_more if not 'Política de devolução' in s]

        #Pegando os preços de mais ofertas 
        for price in soup.find_all(class_='a-price-whole')[1:ofertas]:
            Amazon_price_more.append(price.text)
            Urls_amazon_more.append(url)
            Amazon_title_more.append(title)
            Amazon_installment_price_full.append(installment)

    except:
        pass

#Função final 
def amazon_final(): 

    #Fazendo a primeira função 
    for url in tqdm(urls_dos_produtos):
        search_links(url)

    #Buscando atributos por urls encontradas 
    for url in tqdm(Urls_amazon):
        search_attributes(url)

    #Fazendo o tratamento dos dados 
    #Criando Dataset 
    Dataset_amazon = pd.DataFrame()

    #Colocano os valores na colunas
    Dataset_amazon['Urls'] = Urls_amazon + Urls_amazon_more
    Dataset_amazon['Sellers'] = Amazon_seller + Amazon_seller_more
    Dataset_amazon['Preço'] = Amazon_price + Amazon_price_more
    Dataset_amazon['Loja'] = 'AMAZON'
    Dataset_amazon['ASIN'] = Dataset_amazon['Urls'].str.partition('/dp/')[2].str.partition('/')[0]
    Dataset_amazon['Título'] = Amazon_title + Amazon_title_more
    Dataset_amazon["Installment"] = Amazon_installment_price_full

    Dataset_amazon = Dataset_amazon.drop_duplicates()

    #Limpando a caluna de preço 
    Dataset_amazon['Preço'] = Dataset_amazon['Preço'].str.replace("R","")
    Dataset_amazon['Preço'] = Dataset_amazon['Preço'].str.replace("$","")
    Dataset_amazon['Preço'] = Dataset_amazon['Preço'].str.replace(r"\n","")
    Dataset_amazon['Preço'] = Dataset_amazon['Preço'].str.replace(" ","")
    Dataset_amazon['Preço'] = Dataset_amazon['Preço'].str.replace(".","")
    Dataset_amazon['Preço'] = Dataset_amazon['Preço'].str.replace(",",".")
    Dataset_amazon['Preço'] = Dataset_amazon['Preço'].str.replace("Erro","0")

    #Passando o preço para float
    Dataset_amazon['Preço'] = Dataset_amazon['Preço'].astype('float64')

    #Arrumando os preços de installment
    Dataset_amazon["Parcela"] = Dataset_amazon['Installment'].str.partition("x")[0]
    Dataset_amazon['Parcela'] = Dataset_amazon['Parcela'].str.extract("(\d+)").astype(int)
    Dataset_amazon['Installment'] = Dataset_amazon['Installment'].str.partition("R$")[2]
    Dataset_amazon["Installment"] = Dataset_amazon['Installment'].str.replace("sem juros", "")

    #Colocando a categorização 
    Dataset_amazon['Item'] = Dataset_amazon['Urls'].apply(categorizao)


    #Exportando o arquivo
    Dataset_amazon.to_excel('C:/Users/kcava/OneDrive/Documentos/FIVE C/aplicativo_1.0/Scrappers/Huawei/Downloads/amazon.xlsx', index=False)
























