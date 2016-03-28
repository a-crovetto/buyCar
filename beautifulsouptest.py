import urllib2
from bs4 import BeautifulSoup
import re
import sys    # sys.setdefaultencoding is cancelled by site.py
from collections import Counter
import sqlite3
import datetime
import traceback


reload(sys)    # to re-enable sys.setdefaultencoding()
sys.setdefaultencoding('utf-8')

dolar = 33
whileFlag = True
pageCounter = 1
conn = sqlite3.connect('cars.db')

#fullTechnicalList = []
#fullTechnicalDataList = []
#otherDetailsList = []
fecha = str(datetime.datetime.now().strftime ("%Y-%m-%d"))
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

while (whileFlag):
    url = "http://autos.mercadolibre.com.uy/montevideo/_Desde_"+str(pageCounter)+"_OrderId_PRICE_YearRange_1995-0_PriceRange_62000-320000"
    print url
    try:
        response = opener.open(url)
        page = response.read()

        soup = BeautifulSoup(page, "lxml")
        soup1 = soup.select('#searchResults .article .rowItem .list-view-item-title a')

        regex = re.compile('\#')
        soup2 = [str(s['href']) for s in soup1]
        productUrl = [s for s in soup2 if s not in '#']
        for url in productUrl:
            try:
                c = conn.cursor()

                c.execute("select id from cars where link = '"+url+"'")
                esta = c.fetchone()

                if esta is None:
                    # urlProduct = "http://auto.mercadolibre.com.uy/MLU-433643950-geely-lc-0km-todos-las-versiones-entrega-desde-us-4995-_JM"
                    response = opener.open(url)
                    productPage = response.read()

                    soupProduct = BeautifulSoup(productPage, "lxml")
                    # p = re.compile('http://auto.*"')

                    # precio '.placePrice .ch-price'
                    priceCoin = soupProduct.select('.placePrice .ch-price')
                    priceCoin = str(priceCoin[0].get_text())
                    priceCoin = priceCoin.split( )
                    coin = priceCoin[0]
                    price = priceCoin[1]

                    if coin != 'U$S':
                        price = str(int(float(price))/dolar)

                    # titulo '.cont-tit-description h2'
                    title = soupProduct.select('.cont-tit-description h2')
                    if title == []:
                        title = ''
                    else:
                        title = str(title[0].get_text())

                    # descripcion '#itemDescription'
                    description = soupProduct.select('#itemDescription')
                    description = str(description[0].get_text())

                    # Inserto estos datos
                    c.execute("INSERT INTO cars (Link,Fecha,Precio,Titulo,Descripcion ) VALUES ('"+str(url)+"','"+fecha+"','"+price+"','"+title+"','"+description+"')")

                    # Busco el id recie'n ingresado
                    c.execute("select id from cars where link = '"+url+"'")
                    id = c.fetchone()[0]

                    # veo los datos tecnicos
                    technicalList = soupProduct.select('.technical-details li .tit')
                    technicalList = [s.get_text() for s in technicalList]
                    technicalList = [s.replace(':', '') for s in technicalList]

                    #fullTechnicalList = fullTechnicalList + technicalList

                    technicalDataList = soupProduct.select('.technical-details li strong')
                    technicalDataList = [s.get_text() for s in technicalDataList]

                    #fullTechnicalDataList = fullTechnicalDataList + technicalDataList

                    # Guardo las listas en la base de datos

                    if technicalList is not None:
                        for i in range(0,len(technicalList)):
                            c.execute("INSERT INTO TechnicalDetails (carId, Tipo, Valor ) VALUES ('"+str(id)+"','"+technicalList[i]+"','"+technicalDataList[i]+"')")

                    # Sonido, Confort y seguridad '#techDataHolder .title-details:nth-child(4) span' de a pares los ttulos desde 2
                    # '#techDataHolder .other-details:nth-child(3) span'  listado desde 3
                    othersList = soupProduct.select('#techDataHolder .other-details span')
                    othersList = [s.get_text() for s in othersList]
                    othersList = [s.replace('\t', '') for s in othersList]

                    # otherDetailsList = otherDetailsList + othersList

                    if othersList is not None:
                        for i in range(0,len(othersList)):
                            c.execute("INSERT INTO OtherDetails (carId, detail ) VALUES ('"+str(id)+"','"+othersList[i]+"')")
                    conn.commit()
            except Exception as e:
                print traceback.format_exc()
                print url
        #z = Counter(fullTechnicalList)
        #print z
        #print Counter(fullTechnicalDataList)
        #print Counter(otherDetailsList)
        pageCounter = pageCounter + 48
    except Exception as e:
        whileFlag = False
conn.close()
