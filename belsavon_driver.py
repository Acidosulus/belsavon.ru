from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
from my_library import *
import colorama
from colorama import Fore, Back, Style
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import configparser
from bs4 import BeautifulSoup
from lxml import html
import requests

class WD:
    def init(self):
        self.site_url = 'https://belsavon.ru/'
        config = configparser.ConfigParser()
    def __init__(self):
        self.init()


    def __del__(self):
        try:
            pass
        except: pass


    def Get_HTML(self, curl):
        r = requests.get(curl)
        self.page_source = r.text
        return r.text


    def Get_List_Of_Links_On_Goods_From_Catalog(self, pc_link):
        print(Fore.RED + 'Список товаров каталога: ' + Fore.YELLOW + pc_link + Fore.RESET)
        ll_catalog_items = []
        ll_catalog_items.append(pc_link)
        lc_next_link = pc_link
        for i in range(100):
            lc_next_link = self.Get_Next_Page_Link(lc_next_link)
            if len(lc_next_link)>0:
                ll_catalog_items.append(lc_next_link)
            else:
                break
        return ll_catalog_items

    def Get_Next_Page_Link(self, pc_parent_link):
        self.Get_HTML(pc_parent_link)
        lc_result = ''
        try:
            soup = BeautifulSoup(self.page_source, features='html5lib')
            paginator = soup.find('div', {'class': 'pagination'})
            hrefs_soup = BeautifulSoup(str(paginator.contents[0]), features='html5lib')
            links = hrefs_soup.find_all('a')
            for link in links:
                if 'Вперёд' in link:
                    lc_result = sx(str(link), 'href="/','"')
        except: pass
        return (self.site_url if len(lc_result)>0 else '') + lc_result

    def Get_List_of_Goods_for_Catalog(self, pc_link):
        ll_result = []
        ll_catalogs = self.Get_List_Of_Links_On_Goods_From_Catalog(pc_link)
        for catalog in ll_catalogs:
            ll_items = self.Get_List_of_Goods_from_Catalog_Page(catalog)
            for item in ll_items:
                if item not in ll_result:
                    ll_result.append(item)
        return ll_result

    def Get_List_of_Goods_from_Catalog_Page(self, pc_link:str):
        ll_result = []
        self.Get_HTML(pc_link)
        soup = BeautifulSoup(self.page_source, features='html5lib')
        items = soup.find_all('div', {'class':'item_inner'})
        for item in items:
            lc_link = sx(str(item), '<a href="/','"')
            lc_link = (self.site_url if len(lc_link)>0 else '') + lc_link
            if len(lc_link)>0:
                ll_result.append(lc_link)
        return ll_result

    def Write_To_File(self, cfilename):
        file = open(cfilename, "w", encoding='utf-8')
        file.write(self.page_source)
        file.close()


def Login():
    return WD()


#colorama.init()
#wd = Login()
#print(wd.Get_List_of_Goods_for_Catalog('https://belsavon.ru/'))
