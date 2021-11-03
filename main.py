#Importando as bibliotecas padrão 
import tkinter as tk
import sqlite3
from tkinter.constants import W
from typing import Text
import pandas as pd
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from tqdm import tqdm
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


#Importando função do arquivo de função final do Mercado Livre
from Scrappers.Brands.Urls_faltantes.Urls_Mercado_livre import final_fuction_ML

#Importando funções finais dos scripts de Huawei 
from Scrappers.Huawei.Individuais.amazon import amazon_final
from Scrappers.Huawei.Individuais.b2w import bw2_final
from Scrappers.Huawei.Individuais.magalu import magazine_final
from Scrappers.Huawei.Individuais.ml import ml_final
from Scrappers.Huawei.Individuais.via_varejo import final_via_varejo


#Criando a geometria da página principal 
root = tk.Tk()
root.geometry('300x180')
root.title("Aplicativo Five-C")


### -------------------------------- FUNÇÕES -------------------------------------------- ###

### ---------------------------- ENVIO DE E-MAILS  -------------------------------------- ###

#Página principal enviar e-mail
def mandar_email():
    new_window = tk.Tk()

    new_window.title("Aplicativo de E-mail")

    new_window.geometry('500x100')

    #Colocando área dos textos 
    label_marca = tk.Label(new_window, text="Coloque a sua marca")
    label_marca.grid(row = 1, column= 1, padx=10, pady=10, sticky='W')

    marca = tk.Entry(new_window)
    marca.grid(row = 1, column= 2, padx=10, pady=10, sticky='W')

    label_dia= tk.Label(new_window, text="Coloque a data (Ano-Mes-Dia)")
    label_dia.grid(row = 2, column= 1, padx=10, pady=10, sticky='W')
    
    dia = tk.Entry(new_window)
    dia.grid(row = 2, column= 2, padx=10, pady=10, sticky='W')

    envio = tk.Button(new_window, text='Enviar Email', command=lambda: send_email(marca.get(),dia.get()))
    envio.grid(row=2, column=3, sticky='w')

#FFunção para enviar o e-mail por data e por marca 
def send_email(brand,date):
    #Pegando os dados 
    data = pd.read_excel(r"G:\.shortcut-targets-by-id\1VAK5JIWTmtamcYtBHQGeL7FVwcki0pRp\BRAND PROTECTION\Brand Protection - Daily Report.xlsb", engine='pyxlsb', header=1,convert_float=True)

    #Arrumando a coluna da data 
    data['Date'] = pd.TimedeltaIndex(data['Date'], unit='d') + datetime.datetime(1899,12,30)

    #Limpando a primeira linha que é nula 
    data = data[1:]

    #Filtrando os dados 
    data_filtrada = data[data['Brand'] == brand]
    data_filtrada = data_filtrada[data_filtrada['Status Ad'] == 'Incorrect Ad']
    data_filtrada = data_filtrada[data_filtrada['Part'] == 'Morning']
    data_filtrada = data_filtrada[data_filtrada['Date'] == date]
    data_filtrada = data_filtrada[(data_filtrada['Action'] == 'Adjust Cash Price') | (data_filtrada['Action'] == 'Adjust Installment Price') | (data_filtrada['Action'] == 'Mercado Livre - Take Down') | (data_filtrada['Action'] == 'Send Extrajudicial')]
    data_filtrada = data_filtrada[['Date','Part','Store','Seller','1P X 3P','Suggested Price','Difference','Porcentage','Cash Price','Installment Price','Hiperlink','Item','Action']]
    data_filtrada['Action'] = data_filtrada['Action'].str.replace('Mercado Livre - Take Down','Extrajudicial')
    data_filtrada['Action'] = data_filtrada['Action'].str.replace('Send Extrajudicial','Extrajudicial')
        
    #Exportando o dataset para excel para enviar e-mail 
    data_filtrada.to_excel('./Dados/E-mail/motorola_monitoramento.xlsx', index=False)

    #Logando no servidor do e-mail e mandando o e-mail para os contatos
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    server.login('brandprotection.02@fivec.com.br', 'Five@316712')

    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Motorola Monitoramento - {}'.format(datetime.date.today())
    msg['From'] = 'brandprotection.02@fivec.com.br'
    msg['body'] = 'Linha 1 \n Linha 2 \n Linha 3'
    recipients = ['brandprotection.02@fivec.com.br','brandprotection01@fivec.com.br']
    msg['To'] = ", ".join(recipients)

    part1 = MIMEBase('application','octet-stream')
    part1.set_payload(open('./Dados/E-mail/motorola_monitoramento.xlsx','rb').read())
    encoders.encode_base64(part1)
    part1.add_header('Content-Disposition','attachment;filename="Motorola_monitoramento.xlsx"')

    msg.attach(part1)
    server.sendmail('brandprotection.02@fivec.com.br', recipients, msg.as_string())

### ------------------------------ BUSCA DE URLS  --------------------------------------- ###

#Página para a busca de Url 
def search_urls():
    new_window = tk.Tk()
    new_window.title("Buscando Urls")
    new_window.geometry('300x100')

    #Colocando os botões 
    #Botão para fazer a procura de urls faltantes dentro do Mercado Livre 
    bota_mercado_livre_urls = tk.Button(new_window, text='Urls faltantes Mercado Livre', command=final_fuction_ML)
    bota_mercado_livre_urls.grid(row = 1, column= 1, padx=10, pady=10, sticky='W')

    #Outros Marketplaces
    bota_marketplaces_urls = tk.Button(new_window, text='Urls faltanttes Marketplaces')
    bota_marketplaces_urls.grid(row = 2, column= 1, padx=10, pady=10, sticky='W')

    #Cópia WebPrice
    bota_marketplaces_urls = tk.Button(new_window, text='Cópia WebPrice')
    bota_marketplaces_urls.grid(row = 1, column= 3, padx=10, pady=10, sticky='W')

    #Cópia WebPrice
    bota_marketplaces_urls = tk.Button(new_window, text='Cópia Lett')
    bota_marketplaces_urls.grid(row = 2, column= 3, padx=10, pady=10, sticky='W')

### --------------------------------- DATABASE  ----------------------------------------- ###

#Página principal para ver as opções dos databases
def database():
    new_window = tk.Tk()
    new_window.title("Banco de dados")
    new_window.geometry('200x100')

    #Colocando as opções 
    inserir_botao = tk.Button(new_window, text='Inserir dados', command=database_insert_new_data_page)
    inserir_botao.grid(row = 1, column= 1, padx=10, pady=10, sticky='W')

    manutencao_botao = tk.Button(new_window, text='Ver/Arrumar dados')
    manutencao_botao.grid(row = 2, column= 1, padx=10, pady=10, sticky='W')

#Página para o input dos dados
def database_insert_new_data_page():
    new_window = tk.Tk()
    new_window.title("Inserir dados Banco de dados")
    new_window.geometry('300x100')

    #Colocando a barra da marca 
    brand_text = tk.Label(new_window, text="Coloque a marca")
    brand_text.grid(row = 1, column= 1, padx=10, pady=10, sticky='W')

    brand_choice = tk.Entry(new_window)
    brand_choice.grid(row = 1, column= 2, padx=10, pady=10, sticky='W')

    #Colocando botão para enviar os dados 
    insert = tk.Button(new_window, text='Enviar os dados', command=lambda: database_choice(brand_choice.get()))
    insert.grid(row=2, column=2, sticky='w')

#Função para escolher o database específico
def database_choice(brand):
    if brand == 'gopro':
        database_insert_new_data_gopro()
    elif brand == 'motorola':
        database_insert_new_data_motorola()
    else:
        print("Ocorreu um erro no nome da marca")

#Função para a inserção de dados dentro da tabela de gopro
def database_insert_new_data_gopro():
    #messagem pegando os dados 
    print("---- Pegando os dados do Daily e conectando com o banco de dados ----")

    #Criando o databse 
    database = sqlite3.connect("G:/.shortcut-targets-by-id/1VAK5JIWTmtamcYtBHQGeL7FVwcki0pRp/BRAND PROTECTION/Database/Data/Gopro.db")

    #Criando o cursor 
    c = database.cursor()

    #Abrindo os dados 
    data = pd.read_excel(r"G:\.shortcut-targets-by-id\1VAK5JIWTmtamcYtBHQGeL7FVwcki0pRp\BRAND PROTECTION\Brand Protection - Daily Report.xlsb", engine='pyxlsb', header=1,convert_float=True)
    
    #Arrumando a coluna da data 
    data['Date'] = pd.TimedeltaIndex(data['Date'], unit='d') + datetime.datetime(1899,12,30)

    #Limpando a primeira linha que é nula 
    data = data[1:]

    #Filtrando os dados 
    data_filtrada = data[data['Brand'] == 'GoPro']

    #Pegando apenas as colunas que irei utilizar para a construlão dos dados 
    data_filtrada = data_filtrada[['Store - Seller','Week','Date','Part','Seller','Suggested Price','Cash Price','Installment Price','Hiperlink','Item','Store Status','Store Group','From_To - Sellers','1P X 3P','Store Official?','Seller Official?','Cash Price Status','Installment Price Status','Action','Status Ad','Brand','Ad','Officiality','Item Classification','CUSTOMER CLASSIFICATION','CHANNEL']]

    #Mudando as colunas de Action para corrigir sozinha 
    data_filtrada['Action'] = data_filtrada['Action'].str.replace(r'(^.*In Progress.*$)', 'Mercado Livre - Take Down')
    data_filtrada['Action'] = data_filtrada['Action'].str.replace('Send Extrajudicial', 'Extrajudicial Sent')

    data_filtrada.loc[(data_filtrada['Ad'] == 'Catalog')&(data_filtrada['Action'] == 'Mercado Livre - Take Down'),'Action'] = "ML Catalog - Take Down"

    #Limpando os dados
    data_filtrada['Store - Seller'] = data_filtrada['Store - Seller'].str.replace("'","")

    data_filtrada['Seller'] = data_filtrada['Seller'].str.replace("'","")
    data_filtrada['From_To - Sellers'] = data_filtrada['From_To - Sellers'].str.replace("'","")
    data_filtrada['Item Classification'] = data_filtrada['Item Classification'].str.replace("'","")

    #MESSAGE
    print("Os dados que serão inputados tem os seguintes valores:")
    print("Data inicial: {}\nData final: {}".format(data_filtrada['Date'].min(), data_filtrada['Date'].max()))
    y_n = input("Deseja continuar com a transação (y/n): ")

    if y_n == 'y':

        print("---- Realizando o input dos dados dentro do database ----")

        #Colocando os valores dentro do banco de dados
        for index, row in tqdm(data_filtrada.iterrows()):
            c.execute('''INSERT INTO historic_gopro (Store_Seller,
                                            Week,
                                            Date,
                                            Part,
                                            Seller,
                                            Suggested_price,
                                            Cash_price,
                                            Installment_price,
                                            Hiperlink,
                                            Item,
                                            Store_status,
                                            Store_group,
                                            From_to_sellers,
                                            PXP,
                                            Store_official,
                                            Seller_oficial,
                                            Cash_price_status,
                                            Installment_price_status,
                                            Action,
                                            Status_ad,
                                            Brand,
                                            Ad,
                                            Officiality,
                                            Item_classification,
                                            Customer_classification,
                                            Channel) 
                                values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');'''.format(row['Store - Seller'],
                                                                                                                                                                                row['Week'],
                                                                                                                                                                                row['Date'],
                                                                                                                                                                                row['Part'],
                                                                                                                                                                                row['Seller'],
                                                                                                                                                                                row['Suggested Price'],
                                                                                                                                                                                row['Cash Price'],
                                                                                                                                                                                row['Installment Price'],
                                                                                                                                                                                row['Hiperlink'],
                                                                                                                                                                                row['Item'],
                                                                                                                                                                                row['Store Status'],
                                                                                                                                                                                row['Store Group'],
                                                                                                                                                                                row['From_To - Sellers'],
                                                                                                                                                                                row['1P X 3P'],
                                                                                                                                                                                row['Store Official?'],
                                                                                                                                                                                row['Seller Official?'],
                                                                                                                                                                                row['Cash Price Status'],
                                                                                                                                                                                row['Installment Price Status'],
                                                                                                                                                                                row['Action'],
                                                                                                                                                                                row['Status Ad'],
                                                                                                                                                                                row['Brand'],
                                                                                                                                                                                row['Ad'],
                                                                                                                                                                                row['Officiality'],
                                                                                                                                                                                row['Item Classification'],
                                                                                                                                                                                row['CUSTOMER CLASSIFICATION'],
                                                                                                                                                                                row['CHANNEL']))

        #Dando commit no databse 
        database.commit()

        c.close()

        database.close()

        #message
        print("---- Os dados estão dentro do database ----")

    else:
        print("A transação não ocorreu, tente novamente")   

#Função para a inserção de dados dentro da tabela de motorola
def database_insert_new_data_motorola():
    #messagem pegando os dados 
    print("---- Pegando os dados do Daily e conectando com o banco de dados ----")

    #Criando o databse 
    database = sqlite3.connect("G:/.shortcut-targets-by-id/1VAK5JIWTmtamcYtBHQGeL7FVwcki0pRp/BRAND PROTECTION/Database/Data/Gopro.db")

    #Criando o cursor 
    c = database.cursor()

    #Abrindo os dados 
    data = pd.read_excel(r"G:\.shortcut-targets-by-id\1VAK5JIWTmtamcYtBHQGeL7FVwcki0pRp\BRAND PROTECTION\Brand Protection - Daily Report.xlsb", engine='pyxlsb', header=1,convert_float=True)
    
    #Arrumando a coluna da data 
    data['Date'] = pd.TimedeltaIndex(data['Date'], unit='d') + datetime.datetime(1899,12,30)

    #Limpando a primeira linha que é nula 
    data = data[1:]

    #Filtrando os dados 
    data_filtrada = data[data['Brand'] == 'Motorola']

    #Pegando apenas as colunas que irei utilizar para a construlão dos dados 
    data_filtrada = data_filtrada[['Store - Seller','Week','Date','Part','Seller','Suggested Price','Cash Price','Installment Price','Hiperlink','Item','Store Status','Store Group','From_To - Sellers','1P X 3P','Store Official?','Seller Official?','Cash Price Status','Installment Price Status','Action','Status Ad','Brand']]

    #Limpando os dados
    data_filtrada['Store - Seller'] = data_filtrada['Store - Seller'].str.replace("'","")

    data_filtrada['Seller'] = data_filtrada['Seller'].str.replace("'","")
    data_filtrada['From_To - Sellers'] = data_filtrada['From_To - Sellers'].str.replace("'","")

    #MESSAGE
    print("Os dados que serão inputados tem os seguintes valores:")
    print("Data inicial: {}\nData final: {}".format(data_filtrada['Date'].min(), data_filtrada['Date'].max()))
    y_n = input("Deseja continuar com a transação (y/n): ")

    if y_n == 'y':

        print("---- Colocando os dados dentro do databse ----")

        #Colocando os valores dentro do banco de dados
        for index, row in tqdm(data_filtrada.iterrows()):
            c.execute('''INSERT INTO historic_motorola (Store_Seller,
                                            Week,
                                            Date,
                                            Part,
                                            Seller,
                                            Suggested_price,
                                            Cash_price,
                                            Installment_price,
                                            Hiperlink,
                                            Item,
                                            Store_status,
                                            Store_group,
                                            From_to_sellers,
                                            PXP,
                                            Store_official,
                                            Seller_oficial,
                                            Cash_price_status,
                                            Installment_price_status,
                                            Action,
                                            Status_ad,
                                            Brand) 
                                values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');'''.format(row['Store - Seller'],
                                                                                                                                                                row['Week'],
                                                                                                                                                                row['Date'],
                                                                                                                                                                row['Part'],
                                                                                                                                                                row['Seller'],
                                                                                                                                                                row['Suggested Price'],
                                                                                                                                                                row['Cash Price'],
                                                                                                                                                                row['Installment Price'],
                                                                                                                                                                row['Hiperlink'],
                                                                                                                                                                row['Item'],
                                                                                                                                                                row['Store Status'],
                                                                                                                                                                row['Store Group'],
                                                                                                                                                                row['From_To - Sellers'],
                                                                                                                                                                row['1P X 3P'],
                                                                                                                                                                row['Store Official?'],
                                                                                                                                                                row['Seller Official?'],
                                                                                                                                                                row['Cash Price Status'],
                                                                                                                                                                row['Installment Price Status'],
                                                                                                                                                                row['Action'],
                                                                                                                                                                row['Status Ad'],
                                                                                                                                                                row['Brand']))

        #Dando commit no databse 
        database.commit()

        c.close()

        database.close()
    
        #message
        print("---- Os dados estão dentro do database ----")

    else:
        print("A transação não ocorreu, tente novamente")


### ----------------------------------- HUAWEI ------------------------------------- #### 

#Página inicial das opções dentro da Huawei
def huawei_page():
    new_window = tk.Tk()
    new_window.title("HUAWEI")
    new_window.geometry('210x300')

    #Colocando a barra da marca 
    Text = tk.Label(new_window, text="Coloque os marketplaces:")
    Text.grid(row = 1, column= 1, padx=10, pady=10, sticky='W')

    #Escolhas 
    Text = tk.Label(new_window, text="1 - Amazon")
    Text.grid(row = 2, column= 1, padx=10, pady=0, sticky='W')

    Text = tk.Label(new_window, text="2 - Americanas")
    Text.grid(row = 3, column= 1, padx=10, pady=0, sticky='W')

    Text = tk.Label(new_window, text="3 - Mercado Livre")
    Text.grid(row = 4, column= 1, padx=10, pady=0, sticky='W')

    Text = tk.Label(new_window, text="4 - Magazine Luiza")
    Text.grid(row = 5, column= 1, padx=10, pady=0, sticky='W')

    Text = tk.Label(new_window, text="5 - Via Varejo")
    Text.grid(row = 6, column= 1, padx=10, pady=0, sticky='W')

    Text = tk.Label(new_window, text="6 - Todas")
    Text.grid(row = 7, column= 1, padx=10, pady=0, sticky='W')

    #Escolhas
    Text = tk.Entry(new_window)
    Text.grid(row = 8, column= 1, padx=5, pady=10, ipadx=2 , sticky='W')

    search = tk.Button(new_window, text='Buscar', command=lambda: huawei_choice(Text.get()))
    search.grid(row=8, column=2, sticky='w')

#Função que vai determinar a seleção dos marketplaces
def huawei_choice(marketplace):
    if marketplace == '1':
        try:
            amazon_final()
        except:
            amazon_final()
    elif marketplace == '2':
        try:
            bw2_final()
        except:
            bw2_final()
    elif marketplace == "3":
        try:
            ml_final()
        except:
            ml_final()
    elif marketplace == "4":
        try:
            magazine_final()
        except:
            magazine_final()
    elif marketplace == "5":
        try:
            final_via_varejo()
        except:
            final_via_varejo()
    elif marketplace == "6":
        amazon_final()
        bw2_final()
        ml_final()
        magazine_final()
        final_via_varejo()
    else:
        print("Ocorreu um erro no nome da marca")

### --------------------------------- HOME PAGE  -------------------------------------###

#Criando os botões 
#Colocando o botão de envio de e-mail
botao_email = tk.Button(root, text="Envio de email", command=mandar_email)
botao_email.grid(row = 1, column= 1, padx=10, pady=10, sticky='W')

#Colocando botão visualização dos dados 
botao_database = tk.Button(root, text="Banco de dados", command=database)
botao_database.grid(row = 2, column= 1, padx=10, pady=10, sticky='W')

#Colocando botão buscar as urls 
botao_urls = tk.Button(root, text="Busca de Urls", command=search_urls)
botao_urls.grid(row = 2, column= 2, padx=10, pady=10, sticky='W')

#Huawei
botao_urls = tk.Button(root, text="Huawei", command=huawei_page)
botao_urls.grid(row = 1, column= 2, padx=10, pady=10, sticky='W')

#Fazendo o loop 
root.mainloop()
