from typing import List

from flashscore import converter

from .base import Base
from .league import League


class Country(Base):
    def __init__(self, id: int, name: str, url: str):
        super().__init__()
        
        self.id = id
        self.name = name
        self.url = url
        self.leagues: List[League] = []
        
        self._league_url = 'https://www.flashscore.com/x/req/m_1_'

    def __repr__(self) -> str:
        return "%s(id=%s, name='%s', leagues=%s)" % (
            self.__class__.__name__,
            self.id,
            self.name,
            self.leagues
        )

    def get_leagues(self): 
        flashscore_api_gzip = self.make_request(self._league_url + str(self.id))
        flashscore_api_json = converter.gzip_to_json(flashscore_api_gzip.text)
        
        return sorted([
            League(
                id=league['MTI'],
                name=league['MN'],
                url=f"{self.main_url}{league['MU']}",
                api_endpoint=league['MT'],
            )  
            for league in flashscore_api_json
            if 'MN' in league.keys()
        ], key=lambda league: league.name)
