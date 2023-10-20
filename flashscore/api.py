import json
from typing import List, Optional

from . import converter
from .base import Base
from .country import Country
from .match import Match


class FlashscoreApi(Base):
    def __init__(self, locale: str = 'en'):
        self.locale = locale
        super().__init__(self.locale)
    
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

    def get_today_matches(self, day: Optional[int] = 0) -> List[Match]:
        today_matches_gzip = self.make_request(self._today_matches_url.replace('{day}', str(day)))
        today_matches_json = converter.gzip_to_json(today_matches_gzip.text)
        return [
            Match(id=today_match['AA'], locale=self.locale)
            for today_match in today_matches_json
            if today_match.get('AA') is not None
        ]

    def get_live_matches(self) -> List[Match]:
        today_matches_gzip = self.make_request(self._today_matches_url.replace('{day}', '0'))
        today_matches_json = converter.gzip_to_json(today_matches_gzip.text)

        return [
            Match(id=today_match['AA'], locale=self.locale)
            for today_match in today_matches_json
            if today_match.get('AA') is not None\
            and today_match.get('AB') == '2'
        ]
    
    def get_matches_with_already_loaded_content(self, matches_ids: List[str]) -> List[Match]:
        matches = [ Match(id=id, locale=self.locale) for id in matches_ids ]
        urls = []
        for match in matches:
            urls += [
                match._flashscore_url, 
                match._general_url,
                match._stats_url,
                match._events_url,
                match._odds_url,
                match._head2heads_url,
            ]
        for match, responses in zip(matches, self.split_list_to_chinks(self.make_grequest(urls), 6)):
            match.load_content(*[response.text for response in responses]) 
        return matches
