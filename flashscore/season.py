from typing import List

from . import converter
from .base import Base
from .match import Match


class Season(Base):
    def __init__(self, id: int, title: str, country_id: int, league_id: str):
        super().__init__()
        
        self.id = id
        self.title = title
        self.country_id = country_id
        self.league_id = league_id
        self._matches_url = 'https://local-global.flashscore.ninja/2/x/feed/'
        self._matches_url += f'tr_1_{self.country_id}_{self.league_id}_{self.id}_0_3_en_1'
    def __repr__(self) -> str:
        return "%s(id='%s', title='%s')" % (
            self.__class__.__name__,
            self.id,
            self.title,
        )

    def get_matches_url(self, page: int) -> str:
        return self._matches_url + f'tr_1_{self.country_id}_{self.league_id}_{self.id}_{page}_3_en_1'

    def get_matches_ids(self):
        matches_ids = []
        for response in self.make_grequest([self.get_matches_url(i) for i in range(5)]):
            flashscore_api_json = converter.gzip_to_json(response.text)
            matches = flashscore_api_json
            
            for match in matches: 
                if match.get('AA') is None: continue
                if match.get('AA') in matches_ids: continue
                matches_ids.append(match['AA'])
                
        return matches_ids

    def get_matches(self) -> List[Match]:
        matches_ids = self.get_matches_ids()
        print(matches_ids)
