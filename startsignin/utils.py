import bs4
from bs4 import BeautifulSoup
import requests

amazon_pr = []
amazon_prod = []


def amazon(name,name1,name2):
        global amazon
        #name1 = name.replace(" ","-")
        #name2 = name.replace(" ","+")
        amazon=f'https://www.amazon.in/{name1}/s?k={name2}'
        res = requests.get(f'https://www.amazon.in/{name1}/s?k={name2}',headers=headers)
        soup = BeautifulSoup(res.text,'html.parser')
        amazon_page = soup.select('.a-color-base.a-text-normal')
        amazon_page_length = int(len(amazon_page))
        for i in range(0,amazon_page_length):
            name = name.upper()
            amazon_name = soup.select('.a-color-base.a-text-normal')[i].getText().strip().upper()
            if name in amazon_name:
                amazon_name = soup.select('.a-color-base.a-text-normal')[i].getText().strip()
                amazon_price = soup.select('.a-price-whole')[i].getText().strip().upper()
            break
        amazon_prod.append(amazon_name.text)
        amazon_pr.append(amazon_price.text)

                    
        return amazon_prod,amazon_pr,amazon
amazon(name)