# If you DO have the WhatsApp Desktop app installed
from alright import WhatsApp
from operator import itemgetter
from collections import defaultdict
import datetime
import locale
import json
import pandas as pd
import requests
import sys
import time


locale.setlocale(locale.LC_TIME, 'id_ID.utf8')

OPENING_HOUR = 8
CLOSING_HOUR = 3

cookies = {
    'csrf_cookie_mpos': '5b0c7b868ca031f555e490e9b29fd8de',
    'cookiesession1': '582E227AX2XLTOJCDDGAQX84O1CA8C39',
    'ci_session': 'a%3A4%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%22e1f12245cd75ec9cb853eb10efe2cc47%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A13%3A%2210.100.100.62%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A111%3A%22Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F111.0.0.0+Safari%2F537.36%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1681234190%3B%7Dd6f22faf3f2fdf22bcb4c85ccbe5e18db99b45b5',
}

BRANCH_IDS = {
    'DAGO': 10210,
    'NARIPAN': 14376,
}

DEFAULT_TARGETS = {
    'DAGO': [400, 400, 400, 400, 400, 1000, 500],
    'NARIPAN': [200, 200, 200, 200, 200, 500, 400],
}

TARGETS = {
    'DAGO': int(sys.argv[1]) if len(sys.argv) >= 2 else DEFAULT_TARGETS['DAGO'][datetime.today().weekday()],
    'NARIPAN': int(sys.argv[2]) if len(sys.argv) >= 3 else DEFAULT_TARGETS['NARIPAN'][datetime.today().weekday()],
}

messenger = WhatsApp()


def get_report_date_range():
    now = datetime.datetime.now()
    start_hour = datetime.datetime.today().replace(hour=8, minute=0, second=0, microsecond=0)

    if now.hour < 3:
        return (start_hour - datetime.timedelta(1)), (now-datetime.timedelta(1)).replace(hour=4, minute=0, second=0)
    else:
        return start_hour, now.replace(hour=23, minute=59, second=0)
    

def get_shifting_date():
    now = datetime.datetime.now()

    if now.hour < CLOSING_HOUR:
        return now - datetime.timedelta(1)
    else:
        return now


def get_start_and_end_date():
    now = datetime.datetime.now()

    if now.hour < CLOSING_HOUR:
        return now - datetime.timedelta(1), now
    else:
        return now, now


def get_start_and_end_time():
    now = datetime.datetime.now()

    if now.hour < CLOSING_HOUR:
        return '08:00', '04:00'
    else:
        return '08:00', '23:59'


def get_laporan_sales_by_category(branch_id):
    data = {
        'radio-duration': 'all-day',
        'time-left': '00',
        'time-left': '00',
        'time-right': '00',
        'time-right': '00',
        'branch': str(branch_id),
        'arr_branch': str(branch_id),
        'arr_staff': '',
        'reportrange': f'{startdate} - {enddate}',
        'duration': f'{starttime} - {endtime}',
        'flagEachday': 'false',
        'column': '[{"name":"column[]","value":"category_name"},{"name":"column[]","value":"qty"},{"name":"column[]","value":"void"}]',
        'companyid': '8733',
        'company_type': '0',
    }

    response = requests.post(
        'https://backoffice.dretail.id/mpos-server/index.php/C_report_mt_salesbycategory/exportXls',
        cookies=cookies,
        data=data,
    )

    with open(f'laporan_sales_by_category_{branch_id}.xlsx', 'wb') as f:
        f.write(response.content)
    
    return pd.read_excel(f'laporan_sales_by_category_{branch_id}.xlsx', skiprows=7)


def get_report_salesrealtime_detail(reffnumber):
    data = {
        'reffnumber': reffnumber,
    }

    response = requests.post(
        'https://backoffice.dretail.id/mpos-server/index.php/C_report_salesrealtime/details',
        cookies=cookies,
        data=data,
    )

    opbill_data = json.loads(response.content)
    
    # still unknown why sometimes it returns a list instead of detail
    if type(opbill_data['txnproductitem']) == list:
        return []

    return opbill_data['txnproductitem']['detail']


def get_open_bill(branch_id):
    data = {
        'draw': '1',
        'branch': str(branch_id),
        'status': 'all status',
        'date': 'today',
        'columns[0][name]': '',
        'order[0][column]': '0',
        'order[0][dir]': '',
    }

    response = requests.post(
        'https://backoffice.dretail.id/mpos-server/index.php/C_report_salesrealtime/getData',
        cookies=cookies,
        data=data,
    )

    salesrealtime_data = json.loads(response.content)
    reffnumbers = filter(lambda x: x != '', map(itemgetter('reff_number'), salesrealtime_data['data']))
    open_bills = list(filter(lambda x: len(x) != 0, map(get_report_salesrealtime_detail, reffnumbers)))
    
    # convert into flat list of items
    open_bills = [item for sublist in open_bills for item in sublist]

    ob_items = defaultdict(int)

    for item in open_bills:
        ob_items[item['catName']] += item['qty'] - item['voidQty']
    
    return ob_items


def get_target(branch_name, TOTAL):
    TARGET = TARGETS[branch_name]
    
    if TOTAL > TARGET:
        TARGET = 50 * ((TOTAL // 50) + 1)
    
    return TARGET


def print_items(items):
    MINUMAN = items['ESPRESSO BASED'] + items['POWDER BASED'] + items['MOCKTAIL'] + items['MANUAL BREW'] + items['TEA'] + items['LARGE']
    MAKANAN = items['EATS AND BITES']
    BEER = items['BEER']
    ROKOK = items['ROKOK']
    MERCHANDISE = items['MERCHANDISE']
    PAKET_BUKBER = items['PAKET BUKBER']
    PAKET_PROMO = items['PAKET PROMO']
    EVENT = items['Event']
    PARKIR = items['Parkir']
    TOTAL = MINUMAN + MAKANAN + BEER

    return TOTAL, f'MINUMAN: {MINUMAN}\n' + \
        f'MAKANAN: {MAKANAN}\n' + \
        (f'BEER: {BEER}\n' if BEER else '') + \
        (f'ROKOK: {ROKOK}\n' if ROKOK else '') + \
        (f'MERCHANDISE: {MERCHANDISE}\n' if MERCHANDISE else '') + \
        (f'PAKET/PROMO: {PAKET_PROMO}\n' if PAKET_PROMO else '') + \
        (f'EVENT: {EVENT}\n' if EVENT else '') + \
        (f'PAKET BUKBER: {PAKET_BUKBER}\n' if PAKET_BUKBER else '') + \
        (f'PARKIR: {PARKIR}\n' if PARKIR else '') + \
        f'_*TOTAL: {TOTAL}*_\n'


def get_sales_by_category(branch_name):
    items = defaultdict(int)
    df_laporan_sales = get_laporan_sales_by_category(BRANCH_IDS[branch_name])

    for _, row in df_laporan_sales.iterrows():
        items[row['Category']] += row['Item Sold'] - row['Item Void']

    OPEN_BILL = get_open_bill(BRANCH_IDS[branch_name])

    TOTAL_ITEMS, ITEMS_PRINTS = print_items(items)
    TOTAL_OB, OB_PRINTS = print_items(OPEN_BILL)

    GRAND_TOTAL = TOTAL_ITEMS + TOTAL_OB

    TARGET = get_target(branch_name, GRAND_TOTAL)

    msg = \
        f'*[AUTO] UPDATE ITEM {branch_name}*\n' + \
        f'*{get_shifting_date().strftime("%d %B %Y")}*\n' + \
        f'*TARGET*: {TARGET}\n' + \
        '\n' + \
        '*ITEM*\n' + \
        ITEMS_PRINTS + \
        '\n' + \
        '*OPEN BILL*\n' + \
        OB_PRINTS + \
        '\n' + \
        f'*GRAND TOTAL: {GRAND_TOTAL}*\n' + \
        f'*MINUS: {TARGET - GRAND_TOTAL}*\n'

    print(msg)

    messenger.send_direct_message('XD', msg)


def get_seconds_to_sleep():
    # return seconds to sleep until the next minutes of INTERVAL_IN_MINUTE
    interval_in_minute = max(2, int(sys.argv[3]) if len(sys.argv) >= 4 else 15)
    now = datetime.datetime.now()
    minutes_to_sleep = interval_in_minute - now.minute % interval_in_minute
    return minutes_to_sleep * 60 - now.second


while True:
    startdate, enddate = get_start_and_end_date()
    starttime, endtime = get_start_and_end_time()

    startdate = startdate.strftime('%d/%m/%Y')
    enddate = enddate.strftime('%d/%m/%Y')

    print(f'{startdate} {starttime} - {enddate} {endtime}')

    try:
        get_sales_by_category('DAGO')
    except Exception as e:
        print(e)

    try:
        get_sales_by_category('NARIPAN')
    except Exception as e:
        print(e)
    
    if CLOSING_HOUR <= datetime.datetime.now().hour < OPENING_HOUR:
        break
    
    time.sleep(get_seconds_to_sleep())
