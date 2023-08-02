import requests
import pymysql, re
from urllib import parse, request
from bs4 import BeautifulSoup
import math
import xml.etree.ElementTree as treexml
from datetime import datetime, timedelta
from tqdm import tqdm

conn = pymysql.connect(host="localhost", user="root", password="", db="jodalcheng", port=3306, charset='utf8')

cur = conn.cursor()
cur = conn.cursor(pymysql.cursors.DictCursor)

API_KEY = ""                        # 공공데이터 포털에서 발급받은 API Key 입력 부분
API_URL = "http://apis.data.go.kr/1230000/BidPublicInfoService04"
OPT_NAME_BIDE = "/getBidPblancListInfoServcPPSSrch01?"
EXCLUDE_METHOD = []
BUSINESS_NUM = []
BUSINESS_TRIGGER = False


def get_txt(name, path):
    with open(path, 'r', encoding = "utf-8") as f:
        tmp = f.readlines()
    for i in tmp:
        name.append(i.strip())
    return name

def get_query(category, query_name):
    try:
        tree = treexml.parse('./querys.xml')
        query = tree.find(category)
        return query.find(query_name).text
    except Exception as e:
        print("error detected with {}".format(e))

EXCLUDE_METHOD = get_txt(EXCLUDE_METHOD, './0. exclude_method.txt')
BUSINESS_NUM = get_txt(BUSINESS_NUM, './0. our_business_num.txt')

numOfRows = parse.quote(str(40))
page_no = 1
url = (API_URL + OPT_NAME_BIDE
               + "inqryDiv=1&"
            #    + "inqryBgnDt="+start+"0000&"
            #    + "inqryBgnDt="+"202303010000&"
            #    + "inqryEndDt="+end+"2359&"
            #    + "inqryEndDt="+"202303092359&"
               + "numOfRows="+numOfRows+"&"
               + "ServiceKey="+API_KEY+"&"
               + "pageNo=1"
               )
headers = {
    "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36",
    "Connection": "close"}
req = requests.get(url, headers = headers)
soup = BeautifulSoup(req.text, 'html.parser')
totalCount = soup.find('totalcount')
pageNo = soup.find('pageno')
totalPageNo = math.ceil(int(totalCount.string) / int(numOfRows))
print(totalCount, totalPageNo)

for i in tqdm(range(1, totalPageNo + 1)):
# for i in range(1, totalPageNo + 1):
    url = (API_URL + OPT_NAME_BIDE
               + "inqryDiv=1&"
            #    + "inqryBgnDt="+start+"0000&"
            #    + "inqryBgnDt="+"202303010000&"
            #    + "inqryEndDt="+end+"2359&"
            #    + "inqryEndDt="+"202303082359&"
               + "numOfRows="+numOfRows+"&"
               + "ServiceKey="+API_KEY+"&"
               + "pageNo=" + str(i)
               )
    req = requests.get(url, headers = headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    for itemElement in soup.find_all('item'):
        # if itemElement.cntrctcnclsmthdnm.string != None:
        #     with open("./test.txt", 'a', encoding = 'utf-8') as f:
        #         f.write(itemElement.cntrctcnclsmthdnm.string)
        #         f.write('\n')
        price = itemElement.presmptprce.string
        if price == None:
            price = "0"
        price = format(int(float(price)),',')
        visible = 1
        if itemElement.ntcekindnm.string == '취소':
            visible = 0
        # print(
        #     itemElement.bidntceno.string,               # 공고번호
        #     itemElement.bidntcedt.string,               # 공고일시
        #     itemElement.bidntcenm.string,               # 공고명
        #     itemElement.cntrctcnclsmthdnm.string,       # 계약 방법
        #     itemElement.dminsttnm.string,               # 발주처
        #     price,                                      # 가격
        #     itemElement.bidntcedtlurl.string,            # 공고문주소
        #     itemElement.bidbegindt.string,
        #     itemElement.bidclsedt.string)
        # check_business_num_url = itemElement.bidntcedtlurl.string
        try:
            check_business_num_req = requests.get(itemElement.bidntcedtlurl.string)
            check_soup = BeautifulSoup(check_business_num_req.text, 'html.parser')

            find_business_num = check_soup.find('table', {'summary' : '투찰제한 - 일반'})
            BUSINESS_TRIGGER = False
            if find_business_num != None:
                criterion_business_num = re.compile('[()]+[0-9]+[)]')
                first_arrange_business_num = "".join(criterion_business_num.findall(find_business_num.text))
                second_arrange_business_num = re.findall('\(([^)]+)', first_arrange_business_num)
                result_business_num = list(set(second_arrange_business_num))

                for i in result_business_num:
                    if i in BUSINESS_NUM:
                        BUSINESS_TRIGGER = True
                        break
            else:
                BUSINESS_TRIGGER = True
        except:
            BUSINESS_TRIGGER = True

        if itemElement.cntrctcnclsmthdnm.string not in EXCLUDE_METHOD and BUSINESS_TRIGGER == True:
            # tmp_str = itemElement.bidntceno.string + ', ' + itemElement.bidntcenm.string + ', ' + itemElement.ntcekindnm.string
            # print(itemElement.ntcekindnm.string)
            # print(tmp_str)
            # with open("./test_tmp_str.txt", 'a', encoding = 'utf-8') as f:
            #     f.write(tmp_str)
            #     f.write('\n')
            print("test")
            cur = conn.cursor()
            with conn.cursor() as curs:
                sql = get_query('insert_querys', 'on_duplicate_key_update_notice')
                curs.execute(sql,
                            (
                                itemElement.bidntceno.string,
                                itemElement.bidntcedt.string,
                                itemElement.bidntcenm.string,
                                itemElement.cntrctcnclsmthdnm.string,
                                itemElement.dminsttnm.string,
                                itemElement.bidntcedtlurl.string,
                                datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
                                datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
                                price,
                                itemElement.bidbegindt.string,
                                itemElement.bidclsedt.string,
                                itemElement.opengdt.string,
                                visible,
                                itemElement.bidntcedt.string,
                                itemElement.bidntcenm.string,
                                itemElement.cntrctcnclsmthdnm.string,
                                itemElement.dminsttnm.string,
                                itemElement.bidntcedtlurl.string,
                                datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
                                price,
                                itemElement.bidbegindt.string,
                                itemElement.bidclsedt.string,
                                itemElement.opengdt.string,
                                visible
                            )
                            )
                conn.commit()
