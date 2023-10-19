import asyncio
from typing import List, Optional

import grequests
import requests
from aiohttp import ClientSession


class Base:
    def __init__(self, locale: str = 'en'):
        self._locale_codes = {
            'en': '2',
            'ua': '35',
        }
        self._locale_code = self._locale_codes[locale]
        if locale == 'ua':
            self._main_url = 'https://www.flashscore.ua/'
        else:
            self._main_url = 'https://www.flashscore.com/'
            
        self._league_url = f'https://www.flashscore.com/{self._locale_code}/req/m_1_'
        self._matches_url = 'https://local-global.flashscore.ninja/' + self._locale_code + '/x/feed/tr_{endpoint}_{season}_{page}_3_en_1'
        self._today_matches_url = 'https://local-global.flashscore.ninja/' + self._locale_code + '/x/feed/f_1_{day}_3_en_1'
        self._league_url = f'https://www.flashscore.com/{self._locale_code}/req/m_1_'
        
        self._flashscore_endpoint: str = f"{self._main_url}match/"
        self._general_endpoint: str = f'https://local-global.flashscore.ninja/{self._locale_code}/x/feed/dc_1_'
        self._stats_endpoint: str = f'https://local-global.flashscore.ninja/{self._locale_code}/x/feed/df_st_1_'
        self._events_endpoint: str = f'https://local-global.flashscore.ninja/{self._locale_code}/x/feed/df_sui_1_'
        self._odds_endpoint: str = f'https://2.ds.lsapp.eu/pq_graphql'
        self._head2heads_endpoint: str = f'https://local-global.flashscore.ninja/{self._locale_code}/x/feed/df_hh_1_'
        self._matches_url = f'https://local-global.flashscore.ninja/{self._locale_code}/x/feed/'
            
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
        result = grequests.map([
            grequests.get(url, headers=self._headers)
            for url in urls
        ], gtimeout=20) 
        
        if None in result:
            return self.make_grequest(urls)
        return result

    async def async_requests(self, urls: List[str]) -> List[str]:
        async def async_request(url: str) -> str:
            async with ClientSession() as session:
                try:
                    async with session.get(url, headers=self._headers, timeout=20) as response:
                        return await response.text()
                except asyncio.TimeoutError:
                    async with session.get(url, headers=self._headers, timeout=20) as response:
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
