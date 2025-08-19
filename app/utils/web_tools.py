from typing import List

import requests
from bs4 import BeautifulSoup
from flask import current_app

url = "http://i.whut.edu.cn/xxtg/znbm/hqglc/"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36", }


def get_notice() -> List:
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = 'utf-8'
        result = response.text
        soup = BeautifulSoup(result, 'lxml')
        detail = soup.select_one('div.text_list_cont')
        lis = detail.select('ul.normal_list2 li')
        return [{"title": li.select_one("a").get("title"), "date": li.select_one("strong").get_text()} for li in lis if
                (("停电" in li.select_one("a")["title"]) and (li.select_one("a")["title"].endswith("通知")))]
    except Exception as e:
        current_app.logger.warning(str(e))
        return []
