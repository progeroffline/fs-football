from typing import List, Optional

from flashscore import converter

from .base import Base
from .league import League


class Country(Base):
    def __init__(self, id: int, name: str, url: str, locale: Optional[str] = 'en'):
        self.locale = locale
        super().__init__(self.locale)
        
        self.id = id
        self.name = name
        self.url = url
        self.leagues: List[League] = []

    def __repr__(self) -> str:
        return "%s(id=%s, name='%s', url='%s')" % (
            self.__class__.__name__,
            self.id,
            self.name,
            self.url,
        )

    def get_leagues(self): 
        flashscore_api_gzip = self.make_request(self._league_url + str(self.id))
        flashscore_api_json = converter.gzip_to_json(flashscore_api_gzip.text)
        
        return sorted([
            League(
                id=league['MTI'],
                name=league['MN'],
                url=f"{self.url}{league['MU']}/",
                country_id=self.id,
                api_endpoint=league['MT'],
                country_name=self.name,
            )  
            for league in flashscore_api_json
            if 'MN' in league.keys()
        ], key=lambda league: league.name)
