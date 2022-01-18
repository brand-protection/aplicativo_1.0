#Importando as bibliotecas 
import os
import pandas as pd  
import time
from requests_html import HTML
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import WebDriverException
from tqdm import tqdm
from tqdm import tqdm

#Pegando a variável 
path_direct = os.getcwd()

selenium_97 = path_direct + "\Dados\Selenium\chromedriver_97.exe"
selenium_97 = selenium_97.replace('\\','/')


path_download_urls_huawei = path_direct + "\Scrappers\Huawei\Downloads\Amazon_urls.xlsx"
path_download_urls_huawei = path_download_urls_huawei.replace('\\','/')

#Congiruando o driver 
options = Options()
options.add_argument("--headless")
options.add_argument('--disable-gpu')
options.add_argument("--log-level=3")
options.add_argument('--no-sandbox')
options.add_experimental_option('useAutomationExtension', False)

#Configurando o driver 


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
internacional_list = []
more_offers_list = []

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
    Urls_amazon = [s for s in Urls_amazon if not 'Xiaomi' in s]  
    Urls_amazon = [s for s in Urls_amazon if not 'Asus' in s]  
    Urls_amazon = [s for s in Urls_amazon if not 'TP-Link' in s] 
    Urls_amazon = [s for s in Urls_amazon if not 'D-Link' in s]  
    Urls_amazon = [s for s in Urls_amazon if not 'Tenda' in s]  
    Urls_amazon = [s for s in Urls_amazon if not 'MERCUSYS' in s]  
    Urls_amazon = [s for s in Urls_amazon if not 'Intelbras' in s]  
    Urls_amazon = [s for s in Urls_amazon if not 'adaptador' in s]  
    Urls_amazon = [s for s in Urls_amazon if not 'case' in s]  
    Urls_amazon = [s for s in Urls_amazon if not 'capa' in s]  
    Urls_amazon = [s for s in Urls_amazon if not 'Honor' in s]  
    Urls_amazon = [s for s in Urls_amazon if not 'Onu' in s]  
    Urls_amazon = [s for s in Urls_amazon if not 'P30' in s]  
    Urls_amazon = [s for s in Urls_amazon if not 'watch-3' in s]  
    Urls_amazon = [s for s in Urls_amazon if not 'FreeBuds 3' in s]  
    Urls_amazon = [s for s in Urls_amazon if not 'freebuds-3' in s]  
    Urls_amazon = [s for s in Urls_amazon if not 'Freebuds3' in s]  
    Urls_amazon = [s for s in Urls_amazon if not 'GT2E' in s]  
    Urls_amazon = [s for s in Urls_amazon if not 'AM115' in s]  
    Urls_amazon = [s for s in Urls_amazon if not 'AC1900' in s]  
    Urls_amazon = [s for s in Urls_amazon if not 'CM70-L' in s]

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
        price = soup.find(class_='a-offscreen').text
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

    #Fazendo o try para pegar se a compra é internacional ou não 
    try:
        if soup.find("img", {'src':"https://images-na.ssl-images-amazon.com/images/G/32/foreignseller/Foreign_Seller_Badge_v2._CB403622375_.png"}):
            internacional_list.append("Internacional")
        else:
            internacional_list.append("Nacional")
    except:
        internacional_list.append("Nacional")


    #Fazendo o try para ver se tem mais ofertas 
    try:
        #Fazendo o link de mais ofertas do mesmo produto 
        more_offers = 'https://www.amazon.com.br' + soup.find(class_='a-touch-link a-box olp-touch-link')['href']

        more_offers_list.append(more_offers)
    except:
        pass

#Função para pegar as MORE OFFERS
def search_more_offers(url):    
    #Definindo a variável global 
    global Amazon_seller_more 
    
    
    #Fazendo o requests com o link de mais ofertas 
    driver.get(url)
    time.sleep(2)
    body_el = driver.find_element_by_css_selector('body')
    html_str = body_el.get_attribute('innerHTML')

    #Criando o soup
    soup = BeautifulSoup(html_str, 'html.parser')
    
    amazon_more_seller_correct_list = []

    #Pegando o nome dos sellers 
    for seller in soup.find_all(class_='a-size-small a-link-normal')[3:]:
        Amazon_seller_more.append(seller.text)
        amazon_more_seller_correct_list.append(seller.text)
        

    #Limpando o nome dos sellers 
    Amazon_seller_more = [s for s in Amazon_seller_more if not 'política' in s]
    Amazon_seller_more = [s for s in Amazon_seller_more if not '+' in s]
    Amazon_seller_more = [s for s in Amazon_seller_more if not 'Detalhes' in s]
    Amazon_seller_more = [s for s in Amazon_seller_more if not 'Apagar' in s]
    Amazon_seller_more = [s for s in Amazon_seller_more if not 'Política de devolução' in s]

    amazon_more_seller_correct_list = [s for s in amazon_more_seller_correct_list if not 'política' in s]
    amazon_more_seller_correct_list = [s for s in amazon_more_seller_correct_list if not '+' in s]
    amazon_more_seller_correct_list = [s for s in amazon_more_seller_correct_list if not 'Detalhes' in s]
    amazon_more_seller_correct_list = [s for s in amazon_more_seller_correct_list if not 'Apagar' in s]
    amazon_more_seller_correct_list = [s for s in amazon_more_seller_correct_list if not 'Política de devolução' in s]

    
    int_len = int(len(amazon_more_seller_correct_list))
   

    if int_len > 12:
        int_len = 12
        
    else:
        int_len = int_len + 2

    
    #Pegando o title 
    title = soup.find(class_='aod-asin-title-text-class').text
        
        
    #Pegando os preços de mais ofertas 
    for price in soup.find_all(class_='a-price-whole')[2:int_len]:
        Amazon_price_more.append(price.text)
        Urls_amazon_more.append(url)
        Amazon_title_more.append(title)
        Amazon_installment_price_full.append(Amazon_installment_price_full)


#Função final 
def amazon_final(): 
    global driver 

    driver = webdriver.Chrome(executable_path=selenium_97,options=options)
    driver.delete_all_cookies()

    #Fazendo a primeira função 
    for url in tqdm(urls_dos_produtos):
        search_links(url)

    #Buscando atributos por urls encontradas 
    for url in tqdm(Urls_amazon):
        search_attributes(url)

    for url in tqdm(more_offers_list):
        search_more_offers(url)

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
    #Dataset_amazon['Internacional'] = internacional_list

    #Dataset_amazon = Dataset_amazon.drop_duplicates()

    #Limpando a caluna de preço 
    Dataset_amazon['Preço'] = Dataset_amazon['Preço'].str.replace("R","")
    Dataset_amazon['Preço'] = Dataset_amazon['Preço'].str.replace("$","")
    Dataset_amazon['Preço'] = Dataset_amazon['Preço'].str.replace(r"\n","")
    Dataset_amazon['Preço'] = Dataset_amazon['Preço'].str.replace(" ","")
    Dataset_amazon['Preço'] = Dataset_amazon['Preço'].str.replace(".","")
    Dataset_amazon['Preço'] = Dataset_amazon['Preço'].str.replace(",",".")
    Dataset_amazon['Preço'] = Dataset_amazon['Preço'].str.replace("Erro","0")

    #Passando o preço para float
    #Dataset_amazon['Preço'] = Dataset_amazon['Preço'].astype('float64')

    #Arrumando os preços de installment
    #Dataset_amazon["Parcela"] = Dataset_amazon['Installment'].str.partition("x")[0]
    #Dataset_amazon['Parcela'] = Dataset_amazon['Parcela'].str.extract("(\d+)").astype(int)
    #Dataset_amazon['Installment'] = Dataset_amazon['Installment'].str.partition("R$")[2]
    #Dataset_amazon["Installment"] = Dataset_amazon['Installment'].str.replace("sem juros", "")

    #Colocando a categorização 
    Dataset_amazon['Item'] = Dataset_amazon['Urls'].apply(categorizao)

    print("------------- FINALIZOU AMAZON -----------------")


    #Exportando o arquivo
    Dataset_amazon.to_excel(path_download_urls_huawei, index=False)

























