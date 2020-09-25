import os
import datetime
import csv
import re
import json
import sale_entity
from decimal import Decimal
from requests import get
from lxml import etree
from bs4 import BeautifulSoup

# Read config file
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
config_file = open(os.path.join(__location__, 'config.json'))
config_data = json.load(config_file)

KEYWORDS_EN = config_data['mitsuwa_sales_rader_config']['keywords_en'].split(",")
KEYWORDS_JP = config_data['mitsuwa_sales_rader_config']['keywords_jp'].split(",")

class SaleData:
  def __init__(self):
    pass

  def get_data(self, store):
    try:
      response = get("https://mitsuwa.com/" + store + "/")
      #print(response.text)
      soup = BeautifulSoup(response.text, 'html.parser')

      deals =  soup.find_all(id='DEALS')

      # Get Weekly Special data
      weekly_special_h2 = [s for s in deals if "WEEKLY SPECIAL" in s]

      weekly_special_item_list = []
      ul_index_after_weekly_special = 1

      if(len(weekly_special_h2) > 0):
        weekly_special_div = soup.select_one("#et-boc > div > div.et_pb_section.et_pb_section_1.et_section_regular > div.et_pb_row.et_pb_row_2 > div > div > div > div > div")
        ul_list = weekly_special_div.find_all('ul')
        li_list = []

        for ul in ul_list:
          [li_list.append(li) for li in ul.find_all('li')]

        for li in li_list:
          term = li.find('h3').text.strip()
          price = li.find("div",{"class": "prd-price"}).text.strip()
          title_en = li.select_one("div:nth-child(4) > h2").text.strip()
          title_jpn_underline = li.select_one("div:nth-child(4) > p.title_underline.text_dif_lan")

          if title_jpn_underline != None:
            title_jpn = title_jpn_underline.text.strip() + " " + li.select_one("div:nth-child(4) > p:nth-child(3)").text.strip()
          else:
            title_jpn = li.select_one("div:nth-child(4) > p").text.strip()
          item = sale_entity.SaleEntity(price,title_en,title_jpn,term)

          weekly_special_item_list.append(item)
          ul_index_after_weekly_special = len(ul_list) + 1
      
      # Get other deal data
      deal_item_list = []
      deal_h2 = [s for s in deals if not("WEEKLY SPECIAL" in s)]
      ul_index = ul_index_after_weekly_special
      li_list = []

      if len(deal_h2) > 0:
        term = deal_h2[0].text.strip()
        while soup.select_one(f"#et-boc > div > div.et_pb_section.et_pb_section_1.et_section_regular > div.et_pb_row.et_pb_row_2 > div > div > div > div > ul:nth-child({ul_index})") != None:
          ul = soup.select_one(f"#et-boc > div > div.et_pb_section.et_pb_section_1.et_section_regular > div.et_pb_row.et_pb_row_2 > div > div > div > div > ul:nth-child({ul_index})")
          [li_list.append(li) for li in ul.find_all('li')]
          ul_index += 1

        for li in li_list:
          price = li.find("div",{"class": "prd-price"}).text.replace(" ","")
          title_en = li.select_one("div.prd-heading > h2").text.strip()
          title_jpn_underline = li.select_one("div.prd-heading > p.title_underline.text_dif_lan")
          title_jpn_main = li.select_one("div.prd-heading > p:nth-child(3)")
          title_jpn_span = li.select_one("div.prd-heading > span")

          title_jpn = title_jpn_main.text.strip()

          if title_jpn_underline != None:
            title_jpn = title_jpn_underline.text.strip() + " " + title_jpn

          if title_jpn_span != None:
            title_jpn = title_jpn + " " + title_jpn_span.text.strip()
          item = sale_entity.SaleEntity(price,title_en,title_jpn,term)
          deal_item_list.append(item)


      return weekly_special_item_list,deal_item_list
    except:
      print("An exception occurred")

