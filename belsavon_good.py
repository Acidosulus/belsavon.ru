import base64
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
from my_library import *
from belsavon_driver import *
import colorama
from colorama import Fore, Back, Style
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib import request
from urllib.parse import quote
import wget
import uuid
import configparser
from PIL import Image
import requests
from pathlib import Path
import threading
from bs4 import BeautifulSoup
from lxml import html


def poiskpers(url):
    geourl = '{0}'.format(quote(url))
    return geourl


class Good:
    def __init__(self, ol:WD, lc_link, pc_price:str):
        lc_link = lc_link.replace(r'amp;', '')
        self.pictures = []
        self.sizes = []
        self.prices = []
        self.color = ''
        self.article = ''
        self.name = ''
        self.description= ''
        self.price = ''
        self.brand = ''
        print(Fore.LIGHTGREEN_EX, 'Товар: ', Fore.LIGHTBLUE_EX, lc_link, Fore.RESET)
        self.source = ol.Get_HTML(lc_link)
        ol.Get_HTML(lc_link)
        soup = BeautifulSoup(ol.page_source, features='html5lib')
        
        self.name = soup.find('h1').text
        
        self.price = soup.find('div', 'vina_price').text.strip().replace('руб.','').replace('.00','').replace(' ','')
        if '\n' in self.price:
            self.price = sx('|' + self.price,'|','\n').replace('|','')
        
        self.description =  soup.find('div', {'class':'jshop_prod_description'}).text.strip().replace('\n','').replace('\t','').replace('\r','') + ' ' +\
                            soup.find('div', {'id':'vina-description'}).text.strip().replace('\n','').replace('\t','').replace('\r','')
        if 'У вас должен быть включен' in self.description:
            self.description = self.description[0:self.description.find('У вас должен быть включен')]
        

        pics = soup.find_all('a', {'class':"lightbox"})
        for pic in pics:
            lc_link_on_picture = sx(str(pic), 'href="', '"')
            if lc_link_on_picture not in self.pictures:
                self.pictures.append(lc_link_on_picture)
        