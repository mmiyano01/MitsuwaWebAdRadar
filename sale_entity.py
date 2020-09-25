import os
import datetime
import csv
import re
from decimal import Decimal

class SaleEntity:
  def __init__(self, price, en_name, jp_name, term):
    self.price = price
    self.en_name = en_name
    self.jp_name = jp_name
    self.term = term