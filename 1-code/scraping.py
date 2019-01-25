#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 11:21:59 2019

@author: crilaiun
"""


from selenium import webdriver
import re
import requests
import pandas as pd
import bs4
import time

def obtiene_metricas(pagina,driver):

    driver.get(pagina)
            
    text = ''
    try:
        element=driver.find_element_by_xpath('//*[@class="partial_entry"]')
        text=element.text
    except:
        pass

    user = ''
    try:
        element=driver.find_element_by_xpath('//*[@class="expand_inline scrname"]')
        user = element.text
        
    except:
        pass

    location = ''
    try:
        element=driver.find_element_by_xpath('//*[@class="expand_inline userLocation"]')
        location = element.text
    except:
        pass

    rating = ''
    try:
        #obtengo elemento por nombre de clase
        element=driver.find_element_by_xpath('//*[@class="rating reviewItemInline"]')
        #dentro del elemento obtengo el span y luego que clase tiene asignada para obtener el rating que le dio
        rating_texto = element.find_element_by_xpath('span').get_attribute("class")
        rating = int(re.findall(r'\d', rating_texto)[0])
    except:
        pass    

    date_travel = ''
    try:
        element=driver.find_element_by_xpath('//*[@class="prw_rup prw_reviews_stay_date_hsx"]')
        date_travel = re.findall(r'(?<=Fecha del viaje: )(.*)', element.text)[0]
    except:
        pass

    return text,user,location,rating,date_travel,pagina


#dar grants al ejecutable
#chmod -R 777 /Users/crilaiun/Documents/scrapping_tripadvisor/chromedriver


##############################################################################################################
################################            ##################################################################
################################   LEEME    ##################################################################
################################            ##################################################################
##############################################################################################################
    


#MODIFICAR VARIABLES
    
    #page_root
    #archivo_salida
    #pagina 
    #pag (en el for)
    #directorio del file salida    
    

##############################################################################################################
##############################                ################################################################
##############################   ME LESITE?   ################################################################
##############################                ################################################################
##############################################################################################################    

page_root= 'https://www.tripadvisor.es'
archivo_salida = 'scrapping_emirates'
nombre_areo= 'FlyEmirates'

lista_links=[]

driver = webdriver.Chrome('/Users/crilaiun/Documents/scrapping_tripadvisor/chromedriver')

########### OBTIENE PAGINA PRINCIPAL
#pagina = 'https://www.tripadvisor.es/Airline_Review-d8729069-Reviews-Emirates'
pagina = 'https://www.tripadvisor.es/Airline_Review-d8729069-Reviews-Emirates'

driver.get(pagina)

########### OBTIENE CODIGO DE PAGINA Y CREA LINKS
soup = bs4.BeautifulSoup(driver.page_source, 'lxml')
links = soup.find_all('a', href=True)


########### OBTIENE CANTIDAD DE OFFSETS PAR PAGINACION
links_off = re.findall(r'(?<=<a class="pageNum taLnk" data-offset=")(.*)(?=" data-page-number=)', str(links))
results = [int(i) for i in links_off]
maxpag = max(results)

########### PAGINA PARA OBTENER TODOS LOS LINKS A LOS COMENTARIOS
for i in range(1,int(maxpag/10)+1):
    print(i*10)
    #obtiene pagina de offset
    pag='https://www.tripadvisor.es/Airline_Review-d8729069-Reviews-or{}-Emirates#REVIEWS'.format(str(i*10))
    driver.get(pag)
    #obtiene codigo fuente y agrega links genericos
    soup = bs4.BeautifulSoup(driver.page_source, 'lxml')
    links = soup.find_all('a', href=True)

    #filtra solo links a comentarios aplicando expresiones regulares
    for l in links:
        finds = re.findall(r'(?<=<a href=")(.*)(?=" id=")', str(l))
        for f in finds:
            findrev = re.findall(r'#REVIEWS', f)
            if len(findrev) > 0:
                print(f)
                lista_links.append(f)
    
########### RECORRE LA LISTA DE COMENTARIOS PARA OBTENER DATA


with open('/Users/crilaiun/Documents/scrapping_tripadvisor/'+archivo_salida+'.txt','a',encoding='utf-8') as file:
    file.write('comentario\tusuario\tciudad\tpuntaje\tfecha_viaje\tlink\n')

    count=0
    for o in lista_links:
        count=count+1
        print(str(count))
        print(o)
        try:
            print
            mensaje,usuario,localidad,puntaje,fecha_viaje,link= obtiene_metricas(page_root+o,driver)
            mensaje = re.sub(r"\s+", " ", mensaje, flags=re.UNICODE)
            usuario = re.sub(r"\s+", " ", usuario, flags=re.UNICODE) 
            localidad = re.sub(r"\s+", " ", localidad, flags=re.UNICODE) 
            print(mensaje.strip(),usuario,localidad,puntaje,fecha_viaje,link)
            file.write(mensaje+'\t'+usuario+'\t'+localidad+'\t'+str(puntaje)+'\t'+fecha_viaje+'\t'+link+'\n')
    
        except:
            print('error')
                
            

         




                 