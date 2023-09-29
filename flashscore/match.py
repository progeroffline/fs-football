import json
from dataclasses import dataclass
from datetime import datetime
from typing import Union

from flashscore import converter

from .base import Base


@dataclass()
class StatValue:
    name: str
    home: Union[str, int, float]
    away: Union[str, int, float]

    
@dataclass()
class Odds:
    team: str
    value: float


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
        self.stats_match = self.stats_first_half = self.stats_second_half = None
        self.prematch_home_odds = self.prematch_middle_odds = self.prematch_away_odds = None
        
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
        names, general, stats, events, odds = self.make_grequest([
            self.flashscore_url,
            f'https://local-global.flashscore.ninja/2/x/feed/dc_1_{self.id}',
            f'https://local-global.flashscore.ninja/2/x/feed/df_st_1_{self.id}',
            f'https://local-global.flashscore.ninja/2/x/feed/df_sui_1_{self.id}',
            f'https://2.ds.lsapp.eu/pq_graphql?_hash=ope&eventId={self.id}&projectId=2&geoIpCode=UA&geoIpSubdivisionCode=UA46',
        ])

        self._load_names_content(names.text)
        self._load_general_content(general.text)
        self._load_stats_content(stats.text)
        self._load_events_content(events.text)
        self._load_odds_content(odds.text)
        
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

    def _load_stats_content(self, stats_content: str) -> None:
        stats_match = []
        stats_first_half = []
        stats_second_half = []
        
        # Convert response data to format normal for usage
        stats_json = converter.gzip_to_json(stats_content) 
        
        # Remove {"A1":""} it not used element
        stats_json = stats_json[:len(stats_json)-1]
        
        current_section = 'Match'
        for data in stats_json:
            current_section = data.get('SE') if data.get('SE') is not None else current_section
            if data.get('SE') is not None: continue
            
            if current_section == 'Match':
                stats_match.append(data)
            elif current_section == '1st Half':
                stats_first_half.append(data)
            elif current_section == '2nd Half':
                stats_second_half.append(data)

        self.stats_match = [StatValue(stat['SG'], stat['SH'], stat['SI']) for stat in stats_match]
        self.stats_first_half = [StatValue(stat['SG'], stat['SH'], stat['SI']) for stat in stats_first_half]
        self.stats_second_half = [StatValue(stat['SG'], stat['SH'], stat['SI']) for stat in stats_second_half]

    def _load_events_content(self, events_content: str) -> None:
        pass
        
    def _load_odds_content(self, odds_content: str) -> None:
        odds_json = json.loads(odds_content)
        middle, away, home = odds_json['data']['findPrematchOddsById']['odds'][0]['odds']

        self.prematch_home_odds = Odds('home', float(home['value']))
        self.prematch_away_odds = Odds('away', float(away['value']))
        self.prematch_middle_odds = Odds('middle', float(middle['value']))

        
