from lxml import etree
import time
import requests
import openpyxl
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}


def get_epidemic_info(url):
    response = requests.get(url, headers=headers)
    response.encoding = "utf-8"
    html = etree.HTML(response.text)
    data = []
    result = html.xpath('//script[@type="application/json"]/text()')
    result = result[0]
    result = json.loads(result)
    result = result["component"][0]
    result = result['caseList']
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = '国内疫情'
    sheet.append(['地区', '城市', '新增病例', '累计确诊', '治愈', '死亡'])
    for each in result:
        area_name = [each['area']]
        citys = each['subList']
        for city in citys:
            city_name = [city['city'], city['confirmedRelative'], city['confirmed'], city['crued'], city['died']]
            list_name = area_name + city_name
            for i in list_name:
                if i == "":
                    i = '0'
            sheet.append(list_name)
    wb.save('./dataChina.xlsx')


if __name__ == '__main__':
    url = 'https://voice.baidu.com/act/newpneumonia/newpneumonia/?city=%E4%B8%8A%E6%B5%B7-%E4%B8%8A%E6%B5%B7'
    get_epidemic_info(url)
    time.sleep(1)
