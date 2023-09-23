import json
from datetime import datetime

from flashscore import converter

from .base import Base


class Match(Base):
    def __init__(self, id: str, country_name: str, league_name: str):
        super().__init__()
        
        self.id = id
        self.country_name = country_name
        self.league_name = league_name
        
        self.flashscore_url = f"{self.main_url}/match/{self.id}"
        self.tournament = self.home_team_name = self.away_team_name = None
        self.home_team_name = self.away_team_score = self.timestamp = None
        self.final_total_score = None
        
        # self._load_content()

    def __repr__(self) -> str:
        return "%s(%s)" % (
            self.__class__.__name__,
            ', '.join([
                f"{key}={value}"
                for key, value in vars(self).items()
                if key not in self.private_vars
            ])
        )

    def load_content(self) -> None:
        names, general, events, odds = self.make_grequest([
            self.flashscore_url,
            f'https://local-global.flashscore.ninja/2/x/feed/dc_1_{self.id}',
            f'https://local-global.flashscore.ninja/2/x/feed/df_sui_1_{self.id}',
            f'https://2.ds.lsapp.eu/pq_graphql?_hash=ope&eventId={self.id}&projectId=2&geoIpCode=UA&geoIpSubdivisionCode=UA46',
        ])

        self._load_names_content(names.text)
        self._load_general_content(general.text)
        
    def _load_names_content(self, names_content: str) -> None:
        index_start = names_content.find('window.environment = {') + len('window.environment =')
        index_end = index_start + names_content[index_start:].find('};') + 1
        json_data = json.loads(names_content[index_start:index_end])
        json_data = {
            'header': json_data['header'],
            'home': json_data['participantsData']['home'][0],
            'away': json_data['participantsData']['away'][0],
        }
        
        self.tournament = json_data['header']['tournament']['tournament']
        self.home_team_name = json_data['home']['name']
        self.away_team_name = json_data['away']['name']

    def _load_general_content(self, general_content: str) -> None:
        general_json = converter.gzip_to_json(general_content)[0]
        
        self.timestamp = int(general_json['DC'])
        self.date = datetime.fromtimestamp(self.timestamp)
        self.home_team_score = general_json['DE']
        self.away_team_score = general_json['DF']
        self.final_total_score = f"%s:%s" % (self.home_team_score, self.away_team_score)
