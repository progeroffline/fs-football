import json
from dataclasses import dataclass
from datetime import datetime
from time import time
from typing import List, Optional, Union

from requests import Response

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

    
@dataclass()
class Event:
    type: str
    time: str
    player_name: str 
    player_url: str
    current_score: Optional[str] = None
    second_player_name: Optional[str] = None
    second_player_url: Optional[str] = None
    description: Optional[str] = None
    

    
class Match(Base):
    def __init__(self, id: str, country_name: str, league_name: str):
        super().__init__()
        
        self.id = id
        self.country_name = country_name
        self.league_name = league_name
        
        self.flashscore_url = f"{self.main_url}/match/{self.id}"
        self.tournament = self.home_team_name = self.away_team_name = None
        self.home_team_name = self.away_team_score = self.timestamp = None
        self.final_total_score = self.status = None
        self.stats_match = self.stats_first_half = self.stats_second_half = None
        self.prematch_home_odds = self.prematch_middle_odds = self.prematch_away_odds = None
        self.events = []
        
        # self._load_content()

    def __repr__(self) -> str:
        return "%s(%s)" % (
            self.__class__.__name__,
            ', '.join([
                f"{key}='{value}'" if isinstance(value, (str, datetime)) else f"{key}={value}"
                for key, value in vars(self).items()
                if key not in self.private_vars
            ])
        )

    def _make_requests_to_get_all_match_info(self) -> List[Response]:
        return self.make_grequest([
            self.flashscore_url,
            f'https://local-global.flashscore.ninja/2/x/feed/dc_1_{self.id}',
            f'https://local-global.flashscore.ninja/2/x/feed/df_st_1_{self.id}',
            f'https://local-global.flashscore.ninja/2/x/feed/df_sui_1_{self.id}',
            f'https://2.ds.lsapp.eu/pq_graphql?_hash=ope&eventId={self.id}&projectId=2&geoIpCode=UA&geoIpSubdivisionCode=UA46',
            f'https://local-global.flashscore.ninja/2/x/feed/df_sui_1_{self.id}',
        ])


    def load_content(self) -> None:
        names, general, stats, events, odds, head2heads = self._make_requests_to_get_all_match_info() 
        if any(var is None for var in [names, general, stats, events, odds, head2heads]):
            time.sleep(1)
            names, general, stats, events, odds, head2heads = self._make_requests_to_get_all_match_info()
            
        self._load_names_content(names.text)
        self._load_general_content(general.text)
        self._load_stats_content(stats.text)
        self._load_events_content(events.text)
        self._load_odds_content(odds.text)
        self._load_head2heads_content(head2heads.text)
        
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
        status_codes = {
            '1': 'Not started',
            '2': 'Live',
            '3': 'Ended',
        }
        
        self.timestamp = int(general_json['DC'])
        self.date = datetime.fromtimestamp(self.timestamp)
        self.status = status_codes[general_json['DA']]
        self.home_team_score = general_json['DE'] if general_json.get('DE') is not None else '-'
        self.away_team_score = general_json['DF'] if general_json.get('DF') is not None else '-'
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
        events_json = converter.gzip_to_json(events_content)
        for event in events_json:
            if event.get('III') is None:
                continue
            
            if event['IK'] in ['Goal', 'Substitution - in', 'Substitution - Out']:
                self.events.append(Event(
                    type=event['IK'],
                    time=event['IB'],
                    player_name=event['IF'],
                    player_url=event['IU'],
                    second_player_name=event.get('IF_2'),
                    second_player_url=event.get('IU_2'),
                    current_score=f"{event['INX']}:{event['IOX']}",
                ))
            elif event['IK'] == 'Yellow Card':
                self.events.append(Event(
                    type=event['IK'],
                    time=event['IB'],
                    player_name=event['IF'],
                    player_url=event['IU'],
                    description=event['TL'],
                ))
        
    def _load_odds_content(self, odds_content: str) -> None:
        odds_json = json.loads(odds_content)
        odds = odds_json['data']['findPrematchOddsById']['odds'][0]['odds']
        if len(odds) == 0:
            self.prematch_home_odds = Odds('home', 0.0)
            self.prematch_away_odds = Odds('away', 0.0)
            self.prematch_middle_odds = Odds('middle', 0.0)
            return 

        middle, away, home = odds_json['data']['findPrematchOddsById']['odds'][0]['odds']
        self.prematch_home_odds = Odds('home', float(home['value']))
        self.prematch_away_odds = Odds('away', float(away['value']))
        self.prematch_middle_odds = Odds('middle', float(middle['value']))

    def _load_head2heads_content(self, head2heads: str) -> None:
        pass
