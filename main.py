import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import pywhatkit




def search_product( url_store, tag_html , id_class):
    #requisição
    request = requests.get(url_store)
    soup = BeautifulSoup(request.content, 'html.parser')
    s = soup.find(tag_html, class_= id_class)
    price = s.text

    return price

def datetimes():
    today = datetime.now()
    data_pt = today.strftime('%d/%m/%Y')
    return data_pt


product1 = search_product('https://www.paguemenos.com.br/epidac-oc-sabonete-pele-oleosa-e-ou-acneica-90g/p' , 'span', 'vtex-store-components-3-x-sellingPrice vtex-store-components-3-x-sellingPriceValue t-heading-2-s dib ph2 vtex-store-components-3-x-price_sellingPrice')
date_product1 = datetimes()
product2 = search_product('https://www.extrafarma.com.br/epidac-oc-sabonete-barra-90g/p?idsku=3874' , 'span', 'vtex-store-components-3-x-sellingPrice vtex-store-components-3-x-sellingPriceValue t-heading-2-s dib ph2 vtex-store-components-3-x-price_sellingPrice vtex-store-components-3-x-price_sellingPrice--product-price')
date_product2 = datetimes()


string1 = product1.replace(u'\xa0', u' ')
product_converted = string1.strip("R$ ").replace(',' , '.')
product_converted1 = float(product_converted)
string2 = product2.replace(u'\xa0', u' ')
product_converted2 = string2.strip("R$ ").replace(',' , '.')
product_converted2 = float(product_converted2)


def save_data():
    with open("Search.csv", "a") as archive:
            archive.write(
                f"\nPaguemenos;{product_converted1};{date_product1}\n"
            )
            archive.write(
                f"Extrafarma;{product_converted2};{date_product2}\n"
            )
            

def min_value(archive):
  dataframe = pd.read_csv(archive , delimiter= ';')
  dataframe['VALOR'] = dataframe['VALOR'].astype('float')
  dataframe['DATA DA PESQUISA'] = pd.to_datetime(dataframe['DATA DA PESQUISA'])
  dataframe['DATA DA PESQUISA'] = dataframe['DATA DA PESQUISA'].dt.strftime('%d/%m/%Y')
  price_today = dataframe.VALOR.iloc[-1]
  price_today2 = dataframe.VALOR.iloc[-2]
  store_today = dataframe.LOJA.iloc[-1]
  store_today2 = dataframe.LOJA.iloc[-2]
  price_yesterday = dataframe.VALOR.iloc[-3]
  price_yesterday2 = dataframe.VALOR.iloc[-4]

  if(price_today == price_today2 and price_today == price_yesterday and price_today == price_yesterday2 and price_today2 == price_yesterday and price_today2 == price_yesterday2 and price_yesterday == price_yesterday2):
    pywhatkit.sendwhatmsg_to_group('link_do_grupo' , " Atenção, não houve diminuição nos preços do produto desde ontem" , 7 , 0)
  if(price_today < price_yesterday and price_today2 < price_yesterday2):
    pywhatkit.sendwhatmsg_to_group('link_do_grupo' , f" Atenção, houve diminuição nos preços do produto referente a ontem nas duas loja:\n Loja: {store_today}; Valor: {price_today}\n Loja: {store_today2}; Valor: {price_today2}" , 7 , 0)
  if(price_today < price_yesterday):
    pywhatkit.sendwhatmsg_to_group('link_do_grupo' , f" Atenção, houve diminuição nos preços do produto referente a ontem\n Loja: {store_today}; Valor: {price_today}" , 7 , 0)
  if(price_today2 < price_yesterday2):
    pywhatkit.sendwhatmsg_to_group('link_do_grupo' , f" Atenção, houve diminuição nos preços do produto referente a ontem\n Loja: {store_today2}; Valor: {price_today2}" , 7 , 0)
  if(price_today > price_yesterday and price_today2 > price_yesterday2):
    pywhatkit.sendwhatmsg_to_group('link_do_grupo' , f" Atenção, houve aumento nos preços do produto em ambas as lojas:\n Loja: {store_today}; preço: {price_today}\n Loja: {store_today2}; preço: {price_today2} " , 7 , 0)
  if(price_today > price_yesterday):
    pywhatkit.sendwhatmsg_to_group('link_do_grupo' , f" Atenção, houve aumento nos preços do produto referente a ontem\n Loja: {store_today}; Valor: {price_today}" , 7 , 0)
  if(price_today2 > price_yesterday2):
    pywhatkit.sendwhatmsg_to_group('link_do_grupo' , f" Atenção, houve aumento nos preços do produto referente a ontem\n Loja: {store_today2}; Valor: {price_today2}" , 7 , 0)
  

save_data()
min_value('Search.csv')
