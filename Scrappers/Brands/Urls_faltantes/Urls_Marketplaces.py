#Importando bibliotecas 
import pandas as pd
from pandas.core.frame import DataFrame 
import requests 
import time
from requests.api import request 
from requests_html import HTML
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json as JSON

#Configurando as options do selenium
options = Options()
options.add_argument("--headless")
options.add_argument('--log-level=3')
options.add_argument('--disable-gpu')

#Configurando o driver 
driver = webdriver.Chrome(executable_path=r'C:\Users\kcava\OneDrive\Documentos\FIVE C\aplicativo_1.0\Dados\Selenium\chromedriver_95.exe',options=options)

######################################### MOTOROLA ###############################################

#Listas de urls 
amazon_motorola_urls = []
americanas_motorola_urls = []
carrefour_motorola_urls = []
extra_motorola_urls = []
magalu_motorola_urls = []
store_motorola = []

#FUNÇÕES 
def amazon_motorola():
    #global 
    global amazon_motorola_urls

    #Criando a variável de página 
    paginas = 1 

    #Fazendo o while para pegar das duas páginas 
    while paginas <= 2:
        url_base = 'https://www.amazon.com.br/s?k=babá+eletrônica+motorola&s=price-desc-rank&page={}&__mk_pt_BR=ÅMÅŽÕÑ&crid=1HNNMVLOI8TBI&qid=1628790062&sprefix=babá+ele%2Caps%2C294&ref=sr_pg_2'.format(paginas)

        #Criando o tempo 
        time.sleep(0.3)

        #Pegando o html do site da amazon 
        driver.get(url_base)
        body_el = driver.find_element_by_css_selector('body')
        html_str = body_el.get_attribute('innerHTML')
        html_obj = HTML(html=html_str)

        #Pegar os links da página
        links = [x for x in html_obj.links]

        #Criando os links dos produtos 
        products_links = [f'https://www.amazon.com.br{x}' for x in links]

        #Fazendo o append dos links 
        for link in products_links:
            amazon_motorola_urls.append(link)

        #Acrescentando mais um para a variável página 
        paginas = paginas + 1        

    #Limpando as urls 
    amazon_motorola_urls = [s for s in amazon_motorola_urls if "/dp/" in s]
    amazon_motorola_urls = [s for s in amazon_motorola_urls if "motorola" in s]
    amazon_motorola_urls = [s for s in amazon_motorola_urls if not "carregador" in s]
    amazon_motorola_urls = [s for s in amazon_motorola_urls if not "suporte" in s]
    amazon_motorola_urls = [s for s in amazon_motorola_urls if not "bateria" in s]

    #Colocando o nome da loja 
    for url in amazon_motorola_urls:
        store_motorola.append("AMAZON")

def magalu_motorola():
    #Global 
    global magalu_motorola_urls

    #Tempo
    time.sleep(3)

    #Criando variável de página 
    pagina = 0 

    #Fazendo o loop do while 
    while pagina <= 2:

        #Pegando a url base 
        url = 'https://www.magazineluiza.com.br/busca/baba%20eletronica%20motorola/{}/?ordem=maior-preco'.format(pagina)

        #Fazendo o response 
        response = urlopen(url)
        html = response.read()

        #Criando o soup 
        soup = BeautifulSoup(html, 'html.parser')

        #Achando todos os links 
        for link in soup.find_all("a", href=True):
            magalu_motorola_urls.append(link['href'])

        #Acrescentando o valor para a variável página 
        pagina = pagina + 1 

    #Limpando os links 
    magalu_motorola_urls = [s for s in magalu_motorola_urls if '/p/' in s]

    #Colocando a store 
    for url in magalu_motorola_urls:
        store_motorola.append("MAGAZINE LUIZA")

def americanas_motorola():
    #Global 
    global americanas_motorola_urls

    #Criando a variável de página 
    pag = 1 

    #Criando o loop das páginas 
    while pag <= 216:

        #Criando a url base 
        url_base = "https://www.americanas.com.br/busca/baba-eletronica-motorola?sortBy=higherPrice&limit=24&offset={}".format(pag)

        #Fazendo o tempo 
        time.sleep(3)

        #Pegando os headers 
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.218'}

        #Fazendo o requests 
        response = requests.get(url_base, headers=headers)
        html = response.text

        #Criando o soup 
        bs = BeautifulSoup(html, 'html.parser')

        #Pegando os links 
        for link in bs.find_all('a', href=True):
            americanas_motorola_urls.append("https://www.americanas.com.br" + link['href'])

        #Acrescentando as páginas 
        pag = pag + 24

    #Limpando os links 
    americanas_motorola_urls = [s for s in americanas_motorola_urls if 'produto' in s]

    #Colocando a stroe 
    for url in americanas_motorola_urls:
        store_motorola.append("AMERICANAS")

def extra_motorola():
    #Colocando a variável como global 
    global extra_motorola_urls

    #Url base 
    url = 'https://www.extra.com.br/baba-eletronica-motorola/b?sortby=descprice&'

    #Inicializando o driver na página 
    driver.get(url)

    #Fazendo o while para carregar no botão "Carregar Mais"
    while True:
        try:
            #Encontrando o botão 
            load_more = driver.find_element_by_xpath('//button[text()="Ver mais produtos"]')

            #Esperando carregar o conteúdo da página 
            time.sleep(3)

            #Clicando no botão 
            load_more.click()

            #Experando mais um pouco para carregar o conteúdo do botão 
            time.sleep(2)
        except:
            break

    #Criando o beautiful usando o driver 
    bs = BeautifulSoup(driver.page_source, 'html.parser')

    #Fechando o driver
    driver.close()

    #Pegando os links 
    for link in bs.find_all("a"):
        extra_motorola_urls.append(link['href'])

    #Limpando os links para apenas produtos 
    extra_motorola_urls = [s for s in extra_motorola_urls if 'IdSku=' in s]
    extra_motorola_urls = [s for s in extra_motorola_urls if 'motorola' in s]

    #Colocando a store 
    for link in extra_motorola_urls:
        store_motorola.append("EXTRA")

def carrefour_motorola():
    global carrefour_chaves 

    carrefour_chaves = []

    #Criando variável de página 
    pagina = 1 

    #Fazendo o loop do while 
    while pagina <= 2: 

        #Criando a url 
        url_base = 'https://www.carrefour.com.br/busca/baba%20eletronica%20motorola?order=OrderByTopSaleDESC&page={}'.format(pagina)

        #Criando o tempo 
        time.sleep(10)

        #Configurando o header
        header = {'authority':'www.carrefour.com.br','path':'/busca/estabilizador%20zhiyun?order=OrderByTopSaleDESC&page=1','scheme':'https','accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 OPR/76.0.4017.154'}

        #Fazendo o response 
        respponse = requests.get(url_base, headers=header)
        html = respponse.text
        
        #Criando o beautifulsoap
        bs = BeautifulSoup(html, 'html.parser')

        #Pegar o template para o json 
        template = bs.find('template', attrs={'data-type':'json', 'data-varname':'__STATE__'})

        #Pegando o texto dentro do template 
        text = template.contents[1].string

        #Fazendo o json 
        json = JSON.loads(text)

        #Pegando as chaves dentro da página 
        for key in json:
            carrefour_chaves.append(key)

        #Limpando as chaves 
        carrefour_chaves = [s for s in carrefour_chaves if 'Product' in s]
        carrefour_chaves = [s for s in carrefour_chaves if not 'properties' in s]
        carrefour_chaves = [s for s in carrefour_chaves if not '$' in s]
        carrefour_chaves = [s for s in carrefour_chaves if not 'specificationGroups' in s]
        carrefour_chaves = [s for s in carrefour_chaves if not 'items' in s]

            #Pegando os links dentro de cada chave de produto e construindo o link
        for chaves in carrefour_chaves:
            try:
                carrefour_motorola_urls.append('https://www.carrefour.com.br'+ json[chaves]['link'])
            except:
                pass

        #Acrescentando mais páginas 
        pagina = pagina + 1

    #Colocando o nome da store
    for url in carrefour_motorola_urls:
        store_motorola.append("CARREFOUR")

#PEGANDO OS DADOS 
amazon_motorola()
magalu_motorola()
americanas_motorola()
extra_motorola()
carrefour_motorola()

#Criando o dataframe 
dataframe_motorola = pd.DataFrame()

#Colocando os dados 
dataframe_motorola['Urls'] = amazon_motorola_urls + americanas_motorola_urls + carrefour_motorola_urls + extra_motorola_urls + magalu_motorola_urls
dataframe_motorola['Lojas'] = store_motorola
dataframe_motorola['Marca'] = 'MOTOROLA'
dataframe_motorola['ASIN AMAZON'] = dataframe_motorola['Urls'].str.partition('/dp/')[2].str.partition('/')[0]
dataframe_motorola = dataframe_motorola.drop_duplicates()

#mensagem 
print("Motorola completo")


############################################### GOPRO #################################################

#LISTAS
amazon_gopro_urls = []
americanas_gopro_urls = []
carrefour_gopro_urls = []
extra_gopro_urls = []
magalu_gopro_urls = []
store_gopro = []

#Listas com aas urls para cada hero  
urls_amazon = ['https://www.amazon.com.br/s?k=gopro+hero+8&__mk_pt_BR=ÅMÅŽÕÑ&ref=nb_sb_noss_2','https://www.amazon.com.br/s?k=gopro+hero+9&__mk_pt_BR=ÅMÅŽÕÑ&ref=nb_sb_noss_2','https://www.amazon.com.br/s?k=gopro+max+360&ref=nb_sb_ss_ts-doa-p_1_9']
urls_magazine = ['https://www.magazineluiza.com.br/busca/gopro%20hero%208/','https://www.magazineluiza.com.br/busca/gopro+hero+9/','https://www.magazineluiza.com.br/busca/gopro+max+360/']
urls_americanas = ['https://www.americanas.com.br/busca/gopro-hero-8','https://www.americanas.com.br/busca/gopro-hero-9','https://www.americanas.com.br/busca/gopro-max-360']
urls_extra = ['https://www.extra.com.br/gopro-hero-8/b','https://www.extra.com.br/gopro-hero-9/b','https://www.extra.com.br/gopro-max-360/b']
urls_carrefour = ['https://www.carrefour.com.br/busca/gopro%20hero%208?order=OrderByPriceDESC','https://www.carrefour.com.br/busca/gopro%20hero%209','https://www.carrefour.com.br/busca/gopro%20max%20360']


#FUNÇÕES
def amazon_gopro(url):
    #global 
    global amazon_gopro_urls

    #Criando o tempo 
    time.sleep(3)

    
    driver = webdriver.Chrome(executable_path=r'C:\Users\pedro\Documents\FIVE-C\Aplicativo\project\Dados\Selenium\chromedriver_95.exe',options=options)

    #Pegando o html do site da amazon 
    driver.get(url)
    body_el = driver.find_element_by_css_selector('body')
    html_str = body_el.get_attribute('innerHTML')
    html_obj = HTML(html=html_str)

    #Pegar os links da página
    links = [x for x in html_obj.links]

    #Criando os links dos produtos 
    products_links = [f'https://www.amazon.com.br{x}' for x in links]

    #Fazendo o append dos links 
    for link in products_links:
        amazon_gopro_urls.append(link)

    #Limpando as urls 
    amazon_gopro_urls = [s for s in amazon_gopro_urls if "/dp/" in s]
    amazon_gopro_urls = [s for s in amazon_gopro_urls if "gopro" in s]
    amazon_gopro_urls = [s for s in amazon_gopro_urls if not "suporte" in s]
    amazon_gopro_urls = [s for s in amazon_gopro_urls if not "carregador" in s]
    amazon_gopro_urls = [s for s in amazon_gopro_urls if not "base" in s]
    amazon_gopro_urls = [s for s in amazon_gopro_urls if not "bateria" in s]
    amazon_gopro_urls = [s for s in amazon_gopro_urls if not "lentes" in s]
    amazon_gopro_urls = [s for s in amazon_gopro_urls if not "controle" in s]
    amazon_gopro_urls = [s for s in amazon_gopro_urls if not "case" in s]
    amazon_gopro_urls = [s for s in amazon_gopro_urls if not "adaptador" in s]
    amazon_gopro_urls = [s for s in amazon_gopro_urls if not "mergulho" in s]
    amazon_gopro_urls = [s for s in amazon_gopro_urls if not "flutuador" in s]

def magalu_gopro(url):
    #Global 
    global magalu_gopro_urls

    #Tempo
    time.sleep(3)

    #Fazendo o response 
    response = urlopen(url)
    html = response.read()

    #Criando o soup 
    soup = BeautifulSoup(html, 'html.parser')

    #Achando todos os links 
    for link in soup.find_all("a", href=True):
        magalu_gopro_urls.append(link['href'])

    #Limpando os links 
    magalu_gopro_urls = [s for s in magalu_gopro_urls if '/p/' in s]

def americanas_gopro(url):
    #Global 
    global americanas_gopro_urls

    #Fazendo o tempo 
    time.sleep(3)

    #Pegando os headers 
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.218'}

    #Fazendo o requests 
    response = requests.get(url, headers=headers)
    html = response.text

    #Criando o soup 
    bs = BeautifulSoup(html, 'html.parser')

    #Pegando os links 
    for link in bs.find_all('a', href=True):
        americanas_gopro_urls.append("https://www.americanas.com.br" + link['href'])

    #Limpando os links 
    americanas_gopro_urls = [s for s in americanas_gopro_urls if 'produto' in s]

def extra_gopro(url):
    #Colocando a variável como global 
    global extra_gopro_urls

    #Inicializando o driver na página
    driver = webdriver.Chrome(executable_path=r'C:\Users\pedro\Documents\FIVE-C\Aplicativo\project\Dados\Selenium\chromedriver_95.exe',options=options)
    driver.get(url)

    #Criando o beautiful usando o driver 
    bs = BeautifulSoup(driver.page_source, 'html.parser')

    #Fechando o driver
    driver.close()

    #Pegando os links 
    for link in bs.find_all("a"):
        extra_gopro_urls.append(link['href'])

    #Limpando os links para apenas produtos 
    extra_gopro_urls = [s for s in extra_gopro_urls if 'IdSku=' in s]
    extra_gopro_urls = [s for s in extra_gopro_urls if 'gopro' in s]

def carrefour_gopro(url):
    global carrefour_chaves 

    carrefour_chaves = []

    #Criando o tempo 
    time.sleep(10)

    #Configurando o header
    header = {'authority':'www.carrefour.com.br','path':'/busca/estabilizador%20zhiyun?order=OrderByTopSaleDESC&page=1','scheme':'https','accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 OPR/76.0.4017.154'}

    #Fazendo o response 
    respponse = requests.get(url, headers=header)
    html = respponse.text
    
    #Criando o beautifulsoap
    bs = BeautifulSoup(html, 'html.parser')

    #Pegar o template para o json 
    template = bs.find('template', attrs={'data-type':'json', 'data-varname':'__STATE__'})

    #Pegando o texto dentro do template 
    text = template.contents[1].string

    #Fazendo o json 
    json = JSON.loads(text)

    #Pegando as chaves dentro da página 
    for key in json:
        carrefour_chaves.append(key)

    #Limpando as chaves 
    carrefour_chaves = [s for s in carrefour_chaves if 'Product' in s]
    carrefour_chaves = [s for s in carrefour_chaves if not 'properties' in s]
    carrefour_chaves = [s for s in carrefour_chaves if not '$' in s]
    carrefour_chaves = [s for s in carrefour_chaves if not 'specificationGroups' in s]
    carrefour_chaves = [s for s in carrefour_chaves if not 'items' in s]

        #Pegando os links dentro de cada chave de produto e construindo o link
    for chaves in carrefour_chaves:
        try:
            carrefour_gopro_urls.append('https://www.carrefour.com.br'+ json[chaves]['link'])
        except:
            pass


#PEGANDO OS DADOS 
for url in urls_amazon:
    amazon_gopro(url)

for url in amazon_gopro_urls:
    store_gopro.append("AMAZON")

for url in urls_magazine:
    magalu_gopro(url)

for url in magalu_gopro_urls:
    store_gopro.append("MAGAZINE LUIZA")

for url in urls_americanas:
    americanas_gopro(url)

for url in americanas_gopro_urls:
    store_gopro.append("AMERICANAS")

for url in urls_extra:
    extra_gopro(url)

for url in extra_gopro_urls:
    store_gopro.append("EXTRA")

for url in urls_carrefour:
    carrefour_gopro(url)

for url in carrefour_gopro_urls:
    store_gopro.append("CARREFOUR")

#Criando o dataframe 
dataframe_gopro = pd.DataFrame()

#Colocando os dados 
dataframe_gopro['Urls'] = amazon_gopro_urls + americanas_gopro_urls + carrefour_gopro_urls + extra_gopro_urls + magalu_gopro_urls
dataframe_gopro['Lojas'] = store_gopro
dataframe_gopro['Marca'] = 'GOPRO'
dataframe_gopro['ASIN AMAZON'] = dataframe_gopro['Urls'].str.partition('/dp/')[2].str.partition('/')[0]
dataframe_gopro = dataframe_gopro.drop_duplicates()

#JUNTANDO OS DOIS DATAFRAM E
dataframe_full = pd.concat([dataframe_motorola,dataframe_gopro], ignore_index=True)

#Exportando 
dataframe_full.to_excel("urls.xlsx")









