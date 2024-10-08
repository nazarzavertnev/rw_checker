from bs4 import BeautifulSoup 
import requests 
import schedule 
import time 
from playsound import playsound 
import datetime
import subprocess


import termux as termux

def check(): 
    url = "https://pass.rw.by/ru/route/?from=%D0%9C%D0%B8%D0%BD%D1%81%D0%BA-%D0%9F%D0%B0%D1%81%D1%81%D0%B0%D0%B6%D0%B8%D1%80%D1%81%D0%BA%D0%B8%D0%B9&from_exp=2100001&from_esr=140210&to=%D0%91%D0%BE%D0%B1%D1%80%D1%83%D0%B9%D1%81%D0%BA&to_exp=2100310&to_esr=147008&front_date=8+%D0%BE%D0%BA%D1%82.+2024&date=2024-10-08" 

    try:
        response = requests.get(url) 
    except requests.exceptions.Timeout:
        print("timeout")
        return 0
    except requests.exceptions.TooManyRedirects:
        print("redirects")
        return 0
    except requests.exceptions.RequestException as e:
        print("RequestException")
        return 0
    except requests.exceptions.ConnectionError as e:
        print("connError")
        return 0 

    bs = BeautifulSoup(response.text,"lxml") 

    temp = bs.find('div', {'data-train-id': '1_876Щ_1728405480_1728411780'})
    try:
      temps = temp.find_all('div', {'class': 'sch-table__t-item has-quant'})
    except:
      print('type error')

    output = ""
    output += "----------------------\n"
    output += datetime.datetime.now().strftime("%d.%m %H:%M:%S") + '\n'
    try:
      for t in temps:
          output += "➡️  "
          name = t.find('div', {'class': 'sch-table__t-name'})
          a = t.find('a', {'class': 'sch-table__t-quant js-train-modal dash'})
          if a:
              span = a.find('span')
              if span:
                  output += span.text
          i = t.find('i', {'class': 'quantity-tag svg-tag-special'})
          if not i:
              output += ' ( ✅ ) '
              notify()
          else:
              output += ' ( ♿ ) '
          span_price = t.find('span', {'class': 'js-price'})
          if span_price and span_price.has_attr('data-cost-byn'):
              output += span_price['data-cost-byn'] + ' byn'
          output += '\n'
  
          print(output)
    except:
      print('unknown error')
 
def notify():
    if datetime.datetime.now().hour >= 7 & datetime.datetime.now().hour <= 23:
        print(run_command("termux-notification -t 'Tickets available!' -c 'Check website'"))
        playsound('got.ogg')

def run_command(command):
    process = subprocess.Popen(command, shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    output, error = process.communicate()
    return output, error

schedule.every(1).minutes.do(check) 

while True: 
    schedule.run_pending() 
    time.sleep(1)

#print(temp)


