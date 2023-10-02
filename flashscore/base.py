from typing import List

import grequests
import requests


class Base:
    def __init__(self):
        self._main_url = 'https://flashscore.com/'
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0',
            'Accept': '*/*',
            'Accept-Language': 'en',
            'Referer': 'https://www.flashscore.com/',
            'x-fsign': 'SW9D1eZo',
            'Origin': 'https://www.flashscore.com',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }
    
    def make_request(self, url: str) -> requests.Response:
        return requests.get(url, headers=self._headers) 

    def make_grequest(self, urls: List[str]) -> List[requests.models.Response]:
        return grequests.map([
            grequests.get(url, headers=self._headers)
            for url in urls
        ]) 
