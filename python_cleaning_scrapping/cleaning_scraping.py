# el objetivo de este código es analizar los precios de las zapatillas nike de mujer actuales 
#con los de años anteriores para demostrar que la marca ha subido sus precios


import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from urllib.parse import urljoin
import src.cleaning as c
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


sh=pd.read_csv("../../../data/Datafiniti_Womens_Shoes.csv",encoding = "ISO-8859-1")
sh["brand"]= sh["brand"].map(lambda x: x.lower()) #formateo las marcas para homogeneizarlas
nike= sh.loc[(sh["brand"]== "nike")] #creo un data frame sólo con nike

#depuro lo que no me interesa
nike = nike.drop(['ï»¿id','asins','dimension', 'manufacturer', 'manufacturerNumber', 'prices.merchant', 'prices.offer',
       'prices.returnPolicy', 'prices.shipping', 'colors','prices.size','keys','ean','upc','weight', 'prices.sourceURLs', 'prices.availability', ], axis=1)

#optimizo el formato fecha y separo por año/mes/dia
nike['date']=nike["dateUpdated"].str.extract(r"(\d{4}.\d{2}.\d{2})",)
nike[["an","mes","dia"]]=nike.date.str.split("-",expand=True)

#creo una nueva columna para unificar los modelos de zapatilla
nike["modelo"] = nike["name"].apply(c.modelo)
#exporto los datos filtrados
nike.to_csv("../data_clean/nike_2018.csv")

#creo un nuevo data frame para contatenarlo con los datos que se obtendran del webscrapping
con_2018=nike.loc[:,['an','brand','modelo','prices.amountMax', 'prices.amountMin','prices.isSale']]


#web scraping con selenium


s=Service("/mnt/c/Users/silvi/Desktop/ironhack/proyectos/proyecto2/W3-pipelines-project/proyecto2/jupyter/chromedriver.exe")
url = ('https://www.nike.com/us/es/w/mujeres-calzado-5e1x6zy7ok')
driver = webdriver.Chrome(service=s)
driver.get(url)
time.sleep(1)
driver.find_element_by_xpath("//*[@id='gen-nav-commerce-header-v2']/div[1]/div/div[2]/div/div[2]/div[2]/button").click()
driver.find_element_by_xpath("//*[@id='gen-nav-commerce-header-v2']/aside/div/div/div/div[1]/button").click()

iter=1
while True:
        scrollHeight = driver.execute_script("return document.documentElement.scrollHeight")
        Height=250*iter
        driver.execute_script("window.scrollTo(0, " + str(Height) + ");")
        if Height > scrollHeight:
            print('End of page')
            break
        time.sleep(0.5)
        iter+=1
body = driver.execute_script("return document.body")
source = body.get_attribute('innerHTML') 

soup_sc = BeautifulSoup(source, "html.parser")

productos = soup_sc.findAll("a",{"class": "product-card__link-overlay"})
lista_productos = [producto.getText() for producto in productos]

precios = soup_sc.findAll("div",{"class": "product-price__wrapper css-cl9118"})
lista_precios = [precio.getText() for precio in precios]
lista_precios=[string.lstrip("$") for string in lista_precios]

tipo = soup_sc.findAll("div",{"class": "product-card__subtitle"})
lista_tipo = [ti.getText() for ti in tipo]

link_2021 = soup_sc.findAll("a",{"class": "product-card__link-overlay"})
lista_links = [i['href'] for i in link_2021]

diccionario = {"nombre": lista_productos, "precio":lista_precios, "tipo":lista_tipo, "enlace":lista_links}
data_2021 = pd.DataFrame(diccionario)

data_2021["modelo"] = data_2021["nombre"].apply(c.modelo)

data_2021["an"]="2021"

data_2021["brand"]="nike"

data_2021["prices.amountMax"] = data_2021.precio.apply(c.limpiamos_precio)

data_2021["prices.amountMin"] = data_2021.apply(lambda fila: fila["precio"].split("$")[0], axis=1)

data_2021["prices.isSale"]=data_2021.apply(lambda fila: True if fila["prices.amountMax"]>fila["prices.amountMin"] else False, axis=1)

data_2021["prices.amountMax"]=data_2021["prices.amountMax"].map(lambda x: float(x))
data_2021["prices.amountMin"]=data_2021["prices.amountMin"].map(lambda x: float(x))

data_2021.to_csv("../data_clean/nike_2021.csv")

con_2021=data_2021.loc[:,['an','brand','modelo','prices.amountMax', 'prices.amountMin','prices.isSale']]
nike_prices = pd.concat([con_2018,con_2021])
nike_prices.to_csv("../data_clean/nike_all.csv")
