import datefinder
import re

def get_datetime(text: str) -> str:
    '''
        text:'Đăng ngày 8/06/2022'
        return: '8/06/2022'
    '''
    t = list(datefinder.find_dates(text))[0]
    return f'{t.month}/{t.day}/{t.year}'


def get_price(text: str) -> int:
    '''
        text: '2 Tỷ 450 Triệu'
        return: 2450

        text: '450 Triệu'
        return: 450 
    '''
    st = text.split('Tỷ')
    milion = st[-1].split('Triệu')[0]
    bilion = st[0].strip()
    milion = milion.strip()
    if bilion.isnumeric():
        if milion.isnumeric():
            return int(bilion)*1000 + int(milion)
        else:
            return int(bilion)*1000
    else:
        if milion.isnumeric():
            return  int(milion)
        else:
            return -1


def get_id(text: str) -> int:
    infor = text.split('[')[-1].split(':')[-1]
    infor = infor.split(']')[0]
    return int(infor)


def get_number(text: str) -> int:
    '''
        text: 4 banh
        return: 4
    '''
    try:
        nums = re.findall(r'\b\d+\b', text)
        return int(nums[0])
    except:
        return -1
