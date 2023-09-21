import json
from typing import List

import grequests
import requests

from . import converter, types


class FlashscoreApi:
    def __init__(self):
        self.main_url = 'https://flashscore.com/'
        self.league_url = 'https://www.flashscore.com/x/req/m_1_'
        self.matches_url = 'https://local-global.flashscore.ninja/2/x/feed/tr_1_18_zLQAGOBK_176_3_3_en_1'
        
        self.headers = {
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

    def _make_request(self, url: str) -> requests.Response:
        return requests.get(url, headers=self.headers) 
    
    def get_leagues_matches(self) -> List[types.Match]:
        pass

    def get_all_countries(self) -> List[types.Country]:
        response = self._make_request(self.main_url)
        flashscore_html = response.text         
        raw_data_start = flashscore_html.find('rawData: ') + len('rawData: ')
        raw_data_end = raw_data_start + flashscore_html[raw_data_start:].find('\n') - 1

        json_data = json.loads(flashscore_html[raw_data_start:raw_data_end])
        countries = []
        leagues_urls = []
        for data in json_data:
            for country in data['SCC']:
                leagues_urls.append(grequests.get(self.league_url + str(country['MC'])))
                countries.append(country)
                
        return sorted([
            types.Country(
                id=country['MC'],
                name=country['MCN'],
                url=f"{self.main_url}{country['ML'][1:]}",
                leagues=self.get_country_leagues_from_response(leagues_response),
            )

            for country, leagues_response in zip(countries, grequests.map(leagues_urls))
        ], key=lambda country: country.id)

    def get_country_leagues_from_response(self, response) -> List[types.League]:
        flashscore_api_json = converter.gzip_to_json(response.text)[1:]
        
        return sorted([
            types.League(
                id=league['MTI'],
                name=league['MN'],
                url=league['MU'],
                api_endpoint=league['MT'],
            )
            for league in flashscore_api_json
        ], key=lambda league: league.name)
