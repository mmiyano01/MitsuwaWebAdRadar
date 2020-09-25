import os
import sys
import json
import sale_entity
import sale_data

try:
  # Read config file
  __location__ = os.path.realpath(
      os.path.join(os.getcwd(), os.path.dirname(__file__)))
  config_file = open(os.path.join(__location__, 'config.json'))
  config_data = json.load(config_file)

  # TEST 
  # currenty it only works on Torrance Del AMO store
  store = "td"
  sd = sale_data.SaleData()
  weekly_special_item_list,deal_item_list = sd.get_data(store)

  print ("Weekly Special!!")
  for item in weekly_special_item_list:
    print("-----------------------")
    print(item.term)
    print(item.price)
    print(item.en_name)
    print(item.jp_name)

  print (" ")
  print (" ")
  print (" ")

  print ("Sale Infomation!!")
  for item in deal_item_list:
    print("-----------------------")
    print(item.term)
    print(item.price)
    print(item.en_name)
    print(item.jp_name)

except:
  print("An exception occurred")
