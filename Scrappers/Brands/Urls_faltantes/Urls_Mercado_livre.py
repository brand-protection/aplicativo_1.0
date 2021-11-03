#importando as bibliotecas 
import pandas as pd
from pandas.core.frame import DataFrame 
import time 
from bs4 import BeautifulSoup
from urllib.request import urlopen
import sqlite3
from tqdm import tqdm
import os

def categorizacao(a):
    if 'hero-9' in a:
        return 'HERO 9'
    elif 'hero9' in a:
        return "HERO 9"
    elif 'hero-8' in a:
        return 'HERO 8'
    elif 'hero8' in a:
        return 'HERO 8'
    elif 'gopro-8' in a:
        return 'HERO 8'
    elif 'max' in a:
        return 'MAX 360'
    elif 'hero-10' in a:
        return 'HERO 10'
    elif 'comfort-5' in a:
        return 'Comfort 5'
    elif'Comfort-5' in a:
        return 'Comfort 5'
    elif'comfort5' in a:
        return 'Comfort 5'
    elif'comfort-2' in a:
        return 'Comfort 2'
    elif'comfort-28' in a:
        return 'Comfort 28'
    elif'comfort28' in a:
        return 'Comfort 28'
    elif'mbp-36xl' in a:   
        return "MBP36XL"     
    elif'mbp-36XL' in a:
        return "MBP36XL" 
    elif'mbp36XL' in a:
        return "MBP36XL" 
    elif'mbp36xl' in a:
        return "MBP36XL" 
    elif'mbp-33xl' in a:
        return 'MBP33XL'
    elif'36-xl' in a:
        return 'MBP36XL'
    elif'mbp-33XL' in a:
        return 'MBP33XL'
    elif'mbp33xl' in a:
        return 'MBP33XL'
    elif'mbp33XL' in a:
        return 'MBP33XL'
    elif'33xl' in a:
        return 'mbp33XL'
    elif'mbp-36s' in a:
        return 'MBP36S'
    elif'mbp-36S' in a:
        return 'MBP36S'
    elif'mbp36s' in a:
        return 'MBP36S'
    elif'mbp36S' in a:
        return 'MBP36S'
    elif'mbp-481' in a:
        return 'MBP481'
    elif'mbp481' in a:
        return 'MBP481'
    elif'mbp-622' in a:
        return 'MBP622'
    elif'mbp622' in a:
        return 'MBP622'
    elif'mbp-667' in a:
        return 'MBP667'
    elif'mbp667' in a:
        return 'MBP667'
    elif'mbp-668' in a:
        return 'MBP668'
    elif'mbp668' in a:
        return 'MBP668'
    elif'mbp-855' in a:
        return 'MBP855'
    elif'mbp855' in a:
        return 'MBP855'
    elif'mbp-877' in a:
        return "MBP877"
    elif'mbp877' in a:
        return "MBP877"
    elif'mbp-944' in a:
        return 'MBP944'
    elif'mbp944' in a:
        return 'MBP944'
    elif'mbp-161' in a:
        return 'MBP161'
    elif'mbp161' in a:
        return 'MBP161'
    elif'mbp-163' in a:
        return 'MBP163'
    elif'mbp163' in a:
        return 'MBP163'
    elif'mbp-85sn' in a:
        return 'MBP85sn'
    elif'mbp-85' in a:
        return 'MBP85sn'
    elif'mbp85' in a:
        return 'MBP85sn'
    elif'mbp-38s' in a:
        return 'MBP38s'
    elif'mbp38s' in a:
        return 'MBP38s'
    elif'mbp-88' in a:
        return 'MBP88'
    elif'mbp88' in a:
        return 'MBP88'
    elif'ease-34' in a:
        return 'Ease34'
    elif'ease34' in a:
        return 'Ease34'
    elif'lux-connect-64' in a:
        return 'LUX64 CONNECT'
    elif'lux-64-connect' in a:
        return 'LUX64 CONNECT'
    elif'lux64-connect' in a:
        return 'LUX64 CONNECT'
    elif'lux64connect' in a:
        return 'LUX64 CONNECT'
    elif'LUX64CONNECT' in a:
        return 'LUX64 CONNECT'
    elif'ease-44-connect' in a:
        return 'Ease44'
    elif'ease44-connect' in a:
        return 'Ease44'
    elif'EASE44-connect' in a:
        return 'Ease44'
    elif'mbp30' in a:
        return 'MBP30'
    elif'mbp-30' in a:
        return 'MBP30'
    elif'mbp-482' in a:
        return 'MBP420'
    elif'mbp482' in a:
        return 'MBP482'
    elif'mbp33' in a:
        return 'MBP33S'
    elif'mbp-33' in a:
        return 'MBP33S'
    elif'mbp36' in a:
        return 'MBP36S'
    elif'mbp-36' in a:
        return 'MBP36S'
    elif'easy44' in a:
        return 'Ease44'
    elif'comfort85' in a:
        return 'Comfort85'
    elif'easy34' in a:
        return 'Ease34'
    elif'mpb-855' in a:
        return 'MPB855'
    elif'ease44' in a:
        return 'Ease44'
    elif'mbp844' in a:
        return 'mbp844'
    elif'mbp35' in a:
        return 'mbp35'
    elif'mpb-944' in a:
        return 'MBP944'
    elif'36xl' in a:
        return 'MBP36xl'
    elif'mbp-662' in a:
        return 'MBP662'
    elif'focus66' in a:
        return 'Focus66'
    elif'focus-68' in a:
        return 'Focus68'
    elif'mbp421' in a:
        return 'MBP421'
    elif'mbp-421' in a:
        return 'MBP421'


### GOPRO #####
def links_gopro():
    #Criando as urls de gopro para pesquisar dentro do Mercado Livre
    Urls_base = ['https://cameras.mercadolivre.com.br/novo/gopro-hero-8_OrderId_PRICE*DESC_NoIndex_True',
                 'https://cameras.mercadolivre.com.br/novo/gopro-hero-9_OrderId_PRICE*DESC_NoIndex_True',
                 'https://cameras.mercadolivre.com.br/novo/gopro-hero-10_OrderId_PRICE*DESC_NoIndex_True',
                 'https://cameras.mercadolivre.com.br/novo/gopro-max-360_OrderId_PRICE*DESC_NoIndex_True']

    global Urls_gopro
    Urls_gopro = []

    for url in tqdm(Urls_base):
        soup_products_gopro(url)

def soup_products_gopro(url):
    global Urls_gopro
    
    #Criando tempo 
    time.sleep(2)

    #Criando o response 
    response = urlopen(url)
    html = response.read()

    #Criando o beautiful soup
    bs = BeautifulSoup(html, 'html.parser')

    #Pegando os links de produtos da página 
    for link in bs.find_all("a", href=True):
        Urls_gopro.append(link['href'])

    #Pegando apenas as urls de produtos
    Urls_gopro = [s for s in Urls_gopro if 'tracking_id' in s]

    #Limpando heros antigas
    Urls_gopro = [s for s in Urls_gopro if not 'hero7' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'hero-7' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'hero6' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'hero-7' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'hero-fusion' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'bateria' in s]
    Urls_gopro = [s for s in Urls_gopro if not '-bat-' in s]
    Urls_gopro = [s for s in Urls_gopro if not '-bat-' in s]
    Urls_gopro = [s for s in Urls_gopro if not '1080-hd' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'hero-4' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'hero4' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'media-mod' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'camera-de-sportes' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'remote' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'carregador' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'adaptador' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'suporte' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'capa' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'pelicula' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'bolsa' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'filtro' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'mod' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'case' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'acessorio' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'dome' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'flutuador' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'caixa' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'cartao' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'estabilizador' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'controle' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'feiyutech' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'xiaomi' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'bastao' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'floaty' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'dwaterproof' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'espuma' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'frame' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'braco' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'basto' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'tripe' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'rollcage' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'porta' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'microfone' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'puluz' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'tebru' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'kit-para' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'recarregavel' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'cmera-sportiva-sjcam' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'vidro' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'hero5' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'sport' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'switch' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'caso' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'estrutura' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'protecao' in s]
    Urls_gopro = [s for s in Urls_gopro if not 'tampa' in s]


### MOTOROLA #####
def links_motorola():
    global Urls_motorola

    Url_base_motorola = ['https://lista.mercadolivre.com.br/bebes/seguranca/baba-eletronica/motorola/novo/baba-eletr%C3%B4nica-motorola_OrderId_PRICE*DESC_NoIndex_True#applied_filter_id%3DITEM_CONDITION%26applied_filter_name%3DCondi%C3%A7%C3%A3o%26applied_filter_order%3D7%26applied_value_id%3D2230284%26applied_value_name%3DNovo%26applied_value_order%3D1%26applied_value_results%3D1058']

    Urls_motorola = []

    for url in tqdm(Url_base_motorola):
        soup_products_motorola(url)

def soup_products_motorola(url):
    global Urls_motorola
        
    #Criando tempo 
    time.sleep(2)

    #Criando o response 
    response = urlopen(url)
    html = response.read()

    #Criando o beautiful soup
    bs = BeautifulSoup(html, 'html.parser')

    #Pegando os links de produtos da página 
    for link in bs.find_all("a", href=True):
        Urls_motorola.append(link['href'])

    #Pegando apenas as urls de produtos
    Urls_motorola = [s for s in Urls_motorola if 'tracking_id' in s]

    #Limpando heros antigas
    Urls_motorola = [s for s in Urls_motorola if 'motorola' in s]
    Urls_motorola = [s for s in Urls_motorola if not 'suporte' in s]
    Urls_motorola = [s for s in Urls_motorola if not 'base' in s]
    Urls_motorola = [s for s in Urls_motorola if not 'carregador' in s]
    Urls_motorola = [s for s in Urls_motorola if not 'fonte' in s]
    Urls_motorola = [s for s in Urls_motorola if not 'bateria' in s]
    Urls_motorola = [s for s in Urls_motorola if not 'Orbit' in s]
    Urls_motorola = [s for s in Urls_motorola if not 'orbit' in s]

    #Pegando o botão de página seguinte 
    next_page_button = bs.find(class_='andes-pagination__button andes-pagination__button--next')

    #Fazendo o try para pegar a próxima página 
    try:
        next_page_text = next_page_button.find(class_='andes-pagination__link ui-search-link')['title']

        #Fazendo a condição if 
        if next_page_text == 'Seguinte':
            next_url = next_page_button.find(class_='andes-pagination__link ui-search-link')['href']

            #Refazendo a funçáo com a própria página 
            soup_products_motorola(next_url)
        
        else:
            pass
    except:
        pass


## FINAL ####
def final_fuction_ML():
    global check 
    check = []

    #print
    print("--- Pegando os dados e conectando com o banco de dados ----")

    #Criando o database 
    conn = sqlite3.connect('C:/Users/pedro/Documents/FIVE-C/Aplicativo_tkinter/Scrappers/Brands/Urls_faltantes/Dados/database.db')

    #Criando o cursor
    c = conn.cursor()
    
    links_gopro()

    links_motorola()

    #Concat das duas listas 
    Urls = Urls_gopro + Urls_motorola

    #Criando o dataset 
    dataset = pd.DataFrame()

    #print
    print("---- Limpando os dados encontrados ----")

    #Colocando as urls no dataframe
    dataset['Urls'] = Urls

    #Deletando as duplicadas
    dataset = dataset.drop_duplicates()

    #Colocando os códigos MLB 
    dataset['MLB'] = dataset['Urls'].str[40:50]

    #Criando a coluna de categorização 
    dataset['Item'] = dataset['Urls'].apply(categorizacao)

    #Criando a coluna com os nomes para cadastrar dentro da WebPrice
    dataset['Name'] = dataset["Item"] + " - " + dataset["MLB"]

    #Fazendo o check para ver quais são as urls já cadastradas 
    for codigo in dataset['MLB']:
        c.execute("SELECT 1 FROM Urls WHERE Links='{}';".format(codigo))

        if c.fetchone():
            check.append("ok")
        else:
            check.append("Cadastrar")

    #Colocando o check dentro da tabela 
    dataset['check'] = check

    #Arrumando a ordem do dataset 
    dataset = dataset[["Item","Name","Urls","MLB","check"]]

    #Criando o dataset para cadastrar 
    dataset_cadastrar = dataset[dataset['check'] == "Cadastrar"]

    #Colocando os novos dados dentro do database 
    for row in dataset_cadastrar['MLB']:
        c.execute("INSERT INTO Urls(Links) VALUES('{}')".format(row))

    #Exportando o dataset 
    dataset.to_excel('./Dados/Urls/urls.xlsx', index=False)
    dataset_cadastrar.to_excel('./Dados/Urls/cadastrar.xlsx', index=False)

    print("---- Os dados estão dentro da pasta de E-mail ----")

    #Fazendo o commit do databse 
    conn.commit()

    #Fechando o cursor 
    c.close()

    #Fechando o acesso ao database 
    conn.close()






















































