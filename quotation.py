import requests
import json

URL = "https://api.upbit.com/v1/"
  
class Quotation:
  
  def __init__(self):
    self.__all_markets = self.__get_all_markets()
    
  def __get_all_markets(self):
    url = URL + "market/all?isDetails=true"
    headers = {"accept": "application/json"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != requests.codes.ok:
      response.raise_for_status()
    
    markets = {
      "KRW": [],
      "BTC": [],
      "ETC": [],
    }
    
    for market in response.json():
      if market["market"].startswith("KRW"):
        markets["KRW"].append(market["market"])
      elif market["market"].startswith("BTC"):
        markets["BTC"].append(market["market"])
      else:
        markets["ETC"].append(market["market"])

    return markets
  
  def get_market(self, market: str) -> list:
    return self.__all_markets[market]