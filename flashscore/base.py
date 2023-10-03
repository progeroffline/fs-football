import asyncio
from typing import List

import grequests
import requests
from aiohttp import ClientSession


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

    async def async_requests(self, urls: List[str]) -> List[str]:
        async def async_request(url: str) -> str:
            async with ClientSession() as session:
                async with session.get(url, headers=self._headers) as response:
                    return await response.text()

        tasks_result = []
        async with asyncio.TaskGroup() as tg:
            for url in urls:
                tasks_result.append(tg.create_task(async_request(url)))

        return [r.result() for r in tasks_result]
    
    def make_async_requests(self, urls: List[str]) -> List[str]:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.async_requests(urls))
    
    def split_list_to_chinks(self, lst, chunk_size):
        for i in range(0, len(lst), chunk_size):
            yield lst[i:i + chunk_size]
