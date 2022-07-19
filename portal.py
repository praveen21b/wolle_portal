from read_yaml import read_yaml_file
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from portal_logs import logging
from PortalException import PortalException
import os, sys

class WebScraper():
    

    def __init__(self,file_path:str) -> None:
        try:
            self.schema = read_yaml_file(file_path)
            self.base_url = 'https://www.wollplatz.de/wolle/herstellers'

        except Exception as e:
            raise PortalException(e,sys) from e


    def get_html_page(self,url) -> bs:

        try:
            logging.info(f"The parsing with beasutifulsoup started")
            self.source = requests.get(url).text
            soup = bs(self.source,'html.parser')
            logging.info(f"The parsing with beasutifulsoup complted")
            return soup

        except Exception as e:
            raise PortalException(e,sys) from e



    def get_individual_url(self, url, name:str):
        try:
            soup = self.get_html_page(url)
            #print(len(soup.select('.productlistholder')))
            for element in soup.select('.productlistholder'):
                product_details = element.select_one('.productlist-imgholder')
                #print(product_details['title'])

                product_brand = product_details['title'].split(' ', 1)[0]
                product_name = product_details['title'].split(' ', 1)[1]
                product_url = product_details['href']
                #print(product_brand)
                #print(product_name)
                if product_name == name:
                    logging.info(f"The url of the product found")
                    return product_url

            # if the product not available in page1 then check in next
            if soup.select('li[class=paging-volgende]'):
                logging.info(f"The url from the ")
                #update page number
                current_page_no = int(self.base_url[-1])
                self.base_url = self.base_url[:-1] + str(current_page_no + 1)
                logging.info(f"The url from the {str(current_page_no + 1)} page")
                return self.get_individual_url(self.base_url, name)
        except Exception as e:
            raise PortalException(e,sys) from e
            

    def get_parsed_results(self,url) -> dict:
        try:
            soup = self.get_html_page(url)

            product_title = soup.select_one('#pageheadertitle').text
            #print(product_title)
            product_price = soup.select_one('#ContentPlaceHolder1_upPricePanel').find('span',class_='product-price-amount').text
            product_needle_size = soup.select_one('#pdetailTableSpecs').find('table').find_all('tr')[4].find_all('td')[1].text
            #print(product_needle_size)
            product_composition = soup.select_one('#pdetailTableSpecs').find('table').find_all('tr')[3].find_all('td')[1].text
            #print(product_composition)
            
            mydict = {'brand_name': product_title, 'price': product_price, "needle_size": product_needle_size, "composition": product_composition,'delivery_time': None}
            logging.info(f'The acquired data stored in the dictinary format')
            return mydict
        except Exception as e:
            raise PortalException(e,sys) from e

   
    def output(self):
        try:

            self.dicts = []
            
            soup = self.get_html_page(self.base_url)
            logging.info(f"Checking of availability of the brand started")
            brand_available = False

            for input_brand_name_key in self.schema.keys():
                
                for brands_url_list in soup.select('.productlistholder'):
                    brands_detail = brands_url_list.select_one('.productlist-imgholder') # name, url
                    brands_name = brands_detail['title']
                    brands_url = brands_detail['href']

                    if input_brand_name_key == brands_name:

                        brand_available = True

                        for input_name_key in self.schema[input_brand_name_key]:
                        
                            #print(input_brand_name_key,input_name_key)
                            self.base_url = brands_url
                            # includes page number in the url
                            self.base_url = self.base_url + '?page=' + str(1)

                            # getting bs html page for upadted url
                            product_url = self.get_individual_url(url = self.base_url,name=input_name_key)
                            if product_url:
                                self.base_url = product_url

                                # getting the required details
                                logging.info(f"Required details are gathered.")
                                results = self.get_parsed_results(self.base_url)
                                self.dicts.append(results)           

                            # have to make it more suitable way
                            else:
                                print(f'{input_brand_name_key} not found')

                if not brand_available:
                    logging.info(f'{brands_name}is not available.' )
                brand_available = False
                logging.info(f"details converted into dataframe")
            return  pd.DataFrame(self.dicts)

        except Exception as e:
            raise PortalException(e,sys) from e