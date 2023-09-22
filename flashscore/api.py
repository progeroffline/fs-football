import json
from typing import List

from . import converter
from .base import Base
from .country import Country
from .league import League
from .match import Match


class FlashscoreApi(Base):
    def __init__(self):
        super().__init__()
        
        self._league_url = 'https://www.flashscore.com/x/req/m_1_'
        self._matches_url = 'https://local-global.flashscore.ninja/2/x/feed/tr_{endpoint}_{season}_{page}_3_en_1'
        self._today_matches_url = 'https://local-global.flashscore.ninja/2/x/feed/f_1_0_3_en_1'

    def get_current_league_season(self, league_id: str) -> int:
        flashscore_api_gzip = self.make_request(self._today_matches_url)
        flashscore_api_json = converter.gzip_to_json(flashscore_api_gzip.text)
        print(flashscore_api_json)
    
    def get_league_matches(self, league_id: str) -> List[Match]:
        pass

    def get_countries(self) -> List[Country]:
        response = self.make_request(self.main_url)
        flashscore_html = response.text         
        raw_data_start = flashscore_html.find('rawData: ') + len('rawData: ')
        raw_data_end = raw_data_start + flashscore_html[raw_data_start:].find('\n') - 1

        json_data = json.loads(flashscore_html[raw_data_start:raw_data_end])
        countries = []
        for data in json_data:
            for country in data['SCC']:
                countries.append(Country(
                    id=country['MC'],
                    name=country['MCN'],
                    url=f"{self.main_url}{country['ML'][1:]}",
                ))
                
        return sorted(countries, key=lambda country: country.id)

    def get_country_leagues_from_response(self, response) -> List[League]:
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
