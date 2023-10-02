import json
from typing import List

from .base import Base
from .country import Country


class FlashscoreApi(Base):
    def __init__(self):
        super().__init__()
        
        self._league_url = 'https://www.flashscore.com/x/req/m_1_'
        self._matches_url = 'https://local-global.flashscore.ninja/2/x/feed/tr_{endpoint}_{season}_{page}_3_en_1'
        self._today_matches_url = 'https://local-global.flashscore.ninja/2/x/feed/f_1_0_3_en_1'
    
    def get_countries(self) -> List[Country]:
        response = self.make_request(self._main_url)
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
                    url=f"{self._main_url}{country['ML'][1:]}",
                ))
                
        return sorted(countries, key=lambda country: country.id)
