from lxml import etree
import requests
import pymysql
from datetime import datetime
import time
import urllib3
urllib3.disable_warnings()

class Spider():
    def __init__(self):
        self.base_url = 'https://www.dongchedi.com/motor/pc/car/rank_data'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0'
        }
        self.conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='passwordroot',
            database='cardata',
            charset='utf8mb4'
        )
        self.cursor = self.conn.cursor()

    def parse_url(self, params):
        response = requests.get(self.base_url, params=params, headers=self.headers, verify=False).json()
        return response['data']['list']

    def parse_get_detail(self,series_id):
        url = f'https://www.dongchedi.com/auto/params-carIds-x-{series_id}'
        response = requests.get(url, headers=self.headers, verify=False)
        html = etree.HTML(response.text)
        try:
            level = html.xpath('//div[@data-row-anchor="jb"]/div[2]/div/text()')[0]
        except:
            level = ''
        try:
            fuel_forml = html.xpath('//div[@data-row-anchor="fuel_form"]/div[2]/div/text()')[0]
        except:
            fuel_forml = ''
        try:
            market_time = html.xpath('//div[@data-row-anchor="market_time"]/div[2]/div/text()')[0]
        except:
            market_time = ''
        return level, fuel_forml, market_time

    def parse_get_data(self):
        for i in range(65):
            print(f'正在爬取第 {i+1} 页数据！')
            params = {
                'count': 10,
                'offset': i * 10,
                'rank_data_type': 11
            }
            data_list = self.parse_url(params)
            data_json = []
            for i in data_list:
                level, fuel_forml, market_time = self.parse_get_detail(i['series_id'])
                data_json.append({
                    'series_id': i['series_id'],
                    'series_name': i['series_name'],
                    'image': i['image'],
                    'rank': i['rank'],
                    'min_price': i['min_price'],
                    'max_price': i['max_price'],
                    'count': i['count'],
                    'brand_name': i['brand_name'],
                    'level': level,
                    'fuel_forml':fuel_forml,
                    'market_time':market_time
                })
            self.parse_save_to_db(data_json)
            time.sleep(1)
        self.cursor.close()
        self.conn.close()

    def parse_save_to_db(self,data):
        sql = """
              REPLACE \
              INTO car_data (
               series_id, series_name, image, car_rank, car_count, min_price, max_price,
               brand_name, level, fuel_forml, market_time,crate_time
           ) VALUES (
              %(series_id)s, \
              %(series_name)s, \
              %(image)s, \
              %(rank)s, \
              %(count)s,
              %(min_price)s, \
              %(max_price)s, \
              %(brand_name)s, \
              %(level)s,
              %(fuel_forml)s, \
              %(market_time)s, \
              %(crate_time)s
              ) \
              """
        for item in data:
            item['crate_time'] = datetime.now().date()
        try:
            self.cursor.executemany(sql, data)
            self.conn.commit()
            print(f"成功插入/更新 {len(data)} 条数据")
        except Exception as e:
            self.conn.rollback()
            print("数据库写入失败：", e)


if __name__ == '__main__':
    spider = Spider()
    spider.parse_get_data()
