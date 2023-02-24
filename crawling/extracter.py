import bs4
from bs4 import BeautifulSoup
import urllib.request
from crawling.getter import *
from crawling.norm import *

def extract_detail3(detail: bs4.element.Tag) -> dict:
    dicct = {}
    dicct['price'] = get_price(detail.h1.text.split('-')[-1].strip())
    text =" ".join(detail.div.text.split('\t')[:-1])
    dicct['datetime'] = get_datetime(text)
    return dicct


def extract_detail2(detail: bs4.element.Tag) -> dict:
    text = detail.text
    lst = text.replace('Loading...','').split('»')
    dicct = {}
    if len(lst) == 6:
        dicct['branch'] = norm_branch(lst[2].strip())
        dicct['_class'] = norm_class(lst[3].strip())
        dicct['year_manufacture'] = int(lst[4])
        dicct['_id'] = get_id(lst[5])
    elif len(lst) == 5:
        dicct['branch'] = norm_branch(lst[2].strip())
        dicct['_class'] = norm_class(lst[3].strip())
        dicct['year_manufacture'] = get_number(lst[4])
        dicct['_id'] = get_id(lst[4])
    elif len(lst) == 4:
        dicct['branch'] = norm_branch(lst[2].strip())
        dicct['_class'] = 'other'
        dicct['year_manufacture'] = get_number(lst[3])
        dicct['_id'] = get_id(lst[3])
    return dicct


def extract_detail1(detail: bs4.element.Tag, url: str) -> dict:
    text = detail.text
    list_detail = sorted(text.split('\xa0\t'))
    dicct = {}
    dicct['model'] = norm_model(list_detail[0].split(':')[-1].strip())
    dicct['driver'] = norm_driver(list_detail[1].split(':')[-1].strip())
    dicct['gearbox'] = norm_gearbox(list_detail[3].split(':')[-1].strip())
    dicct['color_exterior'] = list_detail[4].split(':')[-1].strip()
    dicct['color_furniture'] = list_detail[5].split(':')[-1].strip()
    dicct['km'] = norm_km(list_detail[6].split(':')[-1].strip())
    dicct['num_seat'] = get_number(list_detail[7].split(':')[-1])
    dicct['num_door'] = get_number(list_detail[8].split(':')[-1])
    dicct['status'] = norm_status(list_detail[11].split(':')[-1].strip())
    dicct['origin'] = norm_origin(list_detail[12].split(':')[-1].strip())
    dicct['fuel'] = norm_fuel(list_detail[13].split(':')[-1].strip())
    dicct['_url'] = url.strip()
    return dicct


def extract_page(url: str) -> dict:
    url = 'https://bonbanh.com/'+url
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    detail1 = soup.find("div", {"class":"tabbertab"})
    detail2 = soup.find("div", {"class":"breadcrum"})
    detail3 = soup.find("div", {"class":"title"})
    d1 = extract_detail1(detail=detail1, url=url)
    d2 = extract_detail2(detail2)
    d3 = extract_detail3(detail3)
    d1.update(d2)
    d1.update(d3)
    return d1
    