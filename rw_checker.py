from bs4 import BeautifulSoup 
import requests 
import schedule 
import time 
from playsound import playsound 
import datetime


def check(): 
    url = "https://pass.rw.by/ru/route/?from=%D0%9C%D0%B8%D0%BD%D1%81%D0%BA-%D0%9F%D0%B0%D1%81%D1%81%D0%B0%D0%B6%D0%B8%D1%80%D1%81%D0%BA%D0%B8%D0%B9&from_exp=2100001&from_esr=140210&to=%D0%91%D0%BE%D0%B1%D1%80%D1%83%D0%B9%D1%81%D0%BA&to_exp=2100310&to_esr=147008&front_date=5+%D1%81%D0%B5%D0%BD%D1%82.+2024&date=2024-09-05" 

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

    temp = bs.find('div', {'data-train-id': '1_876Б_1725554280_1725560580'})

    temps = temp.find_all('div', {'class': 'sch-table__t-item has-quant'})

    output = ""
    output += "----------------------\n"
    output += datetime.datetime.now().strftime("%d.%m %H:%M:%S") + '\n'

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
        else:
            output += ' ( ♿ ) '
        span_price = t.find('span', {'class': 'js-price'})
        if span_price and span_price.has_attr('data-cost-byn'):
            output += span_price['data-cost-byn'] + ' byn'
        output += '\n'

        print(output)

schedule.every(1).minutes.do(check) 
 
while True: 
    schedule.run_pending() 
    time.sleep(1)

#print(temp)
