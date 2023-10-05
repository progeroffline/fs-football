import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from flashscore import converter

from .base import Base


@dataclass()
class StatValue:
    name: str
    home: Union[str, int, float]
    away: Union[str, int, float]

    
@dataclass()
class Event:
    type: str
    player_name: str 
    player_url: str
    time: Optional[str] = None
    current_score: Optional[str] = None
    second_player_name: Optional[str] = None
    second_player_url: Optional[str] = None
    description: Optional[str] = None
  
    
@dataclass()
class HistoryMatch:
    id: str
    timestamp: int
    date: datetime
    home_team_name: str
    away_team_name: str
    league_name: str
    country: str
    final_total_score: str
    home_team_score: Optional[int] = None
    away_team_score: Optional[int] = None
    main_team: Optional[str] = None
    result_for_main_team: Optional[str] = None
    
    
    
class Match(Base):
    def __init__(self,
                 id: str,
                 country_name: Optional[str] = None,
                 league_name: Optional[str] = None):
        super().__init__()
        
        self.id = id
        self.timestamp: Optional[int] = None
        self.date: Optional[datetime] = None
        self.country_name: Optional[str] = country_name
        self.league_name: Optional[str] = league_name
        self.tournament: Optional[str] = None
        
        self.home_team_name: Optional[str] = None
        self.away_team_name: Optional[str] = None
        self.home_team_score: Optional[int] = None
        self.away_team_score: Optional[int] = None
        
        self.final_total_score: Optional[str] = None
        
        self.status: Optional[str] = None
        
        self.stats_match: List[StatValue] = []
        self.stats_first_half: List[StatValue] = []
        self.stats_second_half: List[StatValue] = []
        
        self.prematch_home_odds: Optional[float] = None
        self.prematch_middle_odds: Optional[float] = None
        self.prematch_away_odds: Optional[float] = None
        
        self.events: List[Event] = [] 
        
        self.home_matches: List[HistoryMatch] = []
        self.away_matches: List[HistoryMatch] = [] 
        self.head2head_matches: List[HistoryMatch] = []

        self._flashscore_url: str = f"{self._main_url}/match/{self.id}"
        self._general_url: str = f'https://local-global.flashscore.ninja/2/x/feed/dc_1_{self.id}'
        self._stats_url: str = f'https://local-global.flashscore.ninja/2/x/feed/df_st_1_{self.id}'
        self._events_url: str = f'https://local-global.flashscore.ninja/2/x/feed/df_sui_1_{self.id}'
        self._odds_url: str = f'https://2.ds.lsapp.eu/pq_graphql?_hash=ope&eventId={self.id}&projectId=2&geoIpCode=UA&geoIpSubdivisionCode=UA46'
        self._head2heads_url: str = f'https://local-global.flashscore.ninja/2/x/feed/df_hh_0_{self.id}'

    def __repr__(self) -> str:
        return "%s(%s)" % (
            self.__class__.__name__,
            ', '.join([
                f"{key}='{value}'" if isinstance(value, (str, datetime)) else f"{key}={value}"
                for key, value in vars(self).items()
                if key[0] != '_' and value is not None and value != []
            ])
        )

    def _make_requests_to_get_all_match_info(self) -> List[str]:
        return self.make_async_requests([
            self._flashscore_url, 
            self._general_url,
            self._stats_url,
            self._events_url,
            self._odds_url,
            self._head2heads_url,
        ])
        
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
        if self.league_name is None: self.league_name = '%s' % self.tournament
        if self.country_name is None:
            self.country_name = json_data['header']['tournament']['category']
            
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
        self.home_team_score = int(general_json['DE']) if general_json.get('DE') is not None else None
        self.away_team_score = int(general_json['DF']) if general_json.get('DF') is not None else None
        if self.home_team_score is None and self.away_team_score is None:
            self.final_total_score = None
        else:
            self.final_total_score = f"%s:%s" % (self.home_team_score, self.away_team_score)

    def _load_stats_content(self, stats_content: str) -> None:
        stats_json = converter.gzip_to_json(stats_content) 
        
        # Remove {"A1":""} it not used element
        stats_json = stats_json[:len(stats_json)-1]
        
        current_section = 'Match'
        for stat in stats_json:
            current_section = stat.get('SE') if stat.get('SE') is not None else current_section
            if stat.get('SE') is not None: continue
            
            if current_section == 'Match':
                self.stats_match.append(StatValue(stat['SG'], stat['SH'], stat['SI']))
            elif current_section == '1st Half':
                self.stats_first_half.append(StatValue(stat['SG'], stat['SH'], stat['SI']))
            elif current_section == '2nd Half':
                self.stats_second_half.append(StatValue(stat['SG'], stat['SH'], stat['SI']))

    def _load_events_content(self, events_content: str) -> None:
        events_json = converter.gzip_to_json(events_content)
        for event in events_json:
            if event.get('III') is None: continue
            if event['IF'] == '' \
                and event['IU'] == '' \
                and event.get('INX') is None \
                and event.get('IOX') is None \
                and event['IK'] == 'Goal':
                    event['IK'] = 'Penaltie'
            
            if event['IK'] == 'Goal':
                self.events.append(Event(
                    type=event['IK'],
                    time=event.get('IB'),
                    player_name=event['IF'],
                    player_url=event['IU'],
                    second_player_name=event.get('IF_2'),
                    second_player_url=event.get('IU_2'),
                    current_score=f"{event['INX']}:{event['IOX']}",
                ))
            elif event['IK'] == 'Penaltie':
                self.events.append(Event(
                    type=event['IK'],
                    time=event.get('IB'),
                    player_name=event['IF'],
                    player_url=event['IU'],
                    second_player_name=event.get('IF_2'),
                    second_player_url=event.get('IU_2'),
                ))
            elif event['IK'] in ['Substitution - in', 'Substitution - Out']:
                self.events.append(Event(
                    type=event['IK'],
                    time=event.get('IB'),
                    player_name=event['IF'],
                    player_url=event['IU'],
                    second_player_name=event.get('IF_2'),
                    second_player_url=event.get('IU_2'),
                ))
            elif event['IK'] == 'Yellow Card':
                self.events.append(Event(
                    type=event['IK'],
                    time=event.get('IB'),
                    player_name=event['IF'],
                    player_url=event['IU'],
                    description=event.get('TL'),
                ))
        
    def _load_odds_content(self, odds_content: str) -> None:
        odds_json = json.loads(odds_content)
        odds = odds_json['data']['findPrematchOddsById']['odds'][0]['odds']
        if len(odds) == 0:
            self.prematch_home_odds = 0.0
            self.prematch_away_odds = 0.0
            self.prematch_middle_odds = 0.0
            return 

        middle, away, home = odds_json['data']['findPrematchOddsById']['odds'][0]['odds']
        self.prematch_home_odds = float(home['value'])
        self.prematch_away_odds = float(away['value'])
        self.prematch_middle_odds = float(middle['value'])

    def _load_head2heads_content(self, head2heads: str) -> None:
        matches_json = converter.gzip_to_json(head2heads) 
        
        # Remove {"A1":""} it not used element
        matches_json = matches_json[:len(matches_json)-1]
        current_section = 0
        results_codes = { 'w': 'Win', 'd': 'Draw', 'lo': 'Loss', 'l': 'Loss'}
        vars_association = {1: self.home_matches, 2: self.away_matches, 3: self.head2head_matches}
        
        for match in matches_json:
            if match.get('KB') is not None: current_section += 1
            if match.get('KP') is None: continue
            if current_section >= 4: break
            
            vars_association[current_section].append(HistoryMatch(
                id=match['KP'],
                timestamp=int(match['KC']),
                date=datetime.fromtimestamp(int(match['KC'])),
                home_team_name=match['FH'],
                home_team_score=int(match['KU']) if match.get('KU') not in [None,''] else None,
                away_team_name=match['FK'],
                away_team_score=int(match['KT']) if match.get('KT') not in [None, ''] else None,
                league_name=match['KF'],
                country=match['KH'],
                final_total_score=match['KL'],
                main_team=match.get('KS'),
                result_for_main_team=results_codes.get(match.get('KN')),
            ))
            
    def load_content(self,
                     names: Optional[Union[str, None]] = None,
                     general: Optional[Union[str, None]] = None,
                     stats: Optional[Union[str, None]] = None,
                     events: Optional[Union[str, None]] = None,
                     odds: Optional[Union[str, None]] = None,
                     head2heads: Optional[Union[str, None]] = None) -> None:
        # First check for None value
        if None in [names, general, stats, events, odds, head2heads]:
            names, general, stats,\
            events, odds, head2heads = self._make_requests_to_get_all_match_info() 
        
        # Second check for None value
        if None in [names, general, stats, events, odds, head2heads]:
            names, general, stats,\
            events, odds, head2heads = self._make_requests_to_get_all_match_info()
        
        # Third check for None value
        if names is None or\
            general is None or\
            stats is None or\
            events is None or\
            odds is None or\
            head2heads is None:
            return 
            
        self._load_names_content(names)
        self._load_general_content(general)
        self._load_stats_content(stats)
        self._load_events_content(events)
        self._load_odds_content(odds)
        self._load_head2heads_content(head2heads)
     
    def get_json(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            'date': str(self.date),
            'country_name': self.country_name,
            'league_name': self.league_name,
            'tournament': self.tournament,
            'home_team_name': self.home_team_name,
            'away_team_name': self.away_team_name,
            'home_team_name': self.home_team_score,
            'away_team_score': self.away_team_score,
            'final_total_score': self.final_total_score,
            'status': self.status,
            'stats_match': [
                {
                    'name': stats.name,
                    'home': stats.home,
                    'away': stats.away,
                }
                for stats in self.stats_match
            ],
            'stats_first_half': [
                {
                    'name': stats.name,
                    'home': stats.home,
                    'away': stats.away,
                }
                for stats in self.stats_first_half
            ],
            'stats_second_half': [
                {
                    'name': stats.name,
                    'home': stats.home,
                    'away': stats.away,
                }
                for stats in self.stats_second_half
            ],
            'prematch_home_odds': self.prematch_home_odds,
            'prematch_middle_odds': self.prematch_middle_odds,
            'prematch_away_odds': self.prematch_away_odds,
            'events': [
                {
                    'type': event.type,
                    'player_name': event.player_name,
                    'player_url': event.player_url,
                    'time': event.time,
                    'current_score': event.current_score,
                    'second_player_name': event.second_player_name,
                    'second_player_url': event.second_player_url,
                    'description': event.description,
                } 
                for event in self.events
            ],
            'home_matches': [
                {
                    'id': match.id,
                    'timestamp': match.timestamp,
                    'date': str(match.date),
                    'home_team_name': match.home_team_name,
                    'home_team_score': match.home_team_score,
                    'away_team_name': match.away_team_name,
                    'away_team_score': match.away_team_score,
                    'league_name': match.league_name,
                    'country': match.country,
                    'final_total_score': match.final_total_score,
                    'main_team': match.main_team,
                    'result_for_main_team': match.result_for_main_team,
                }
                for match in self.home_matches
            ],
            'away_matches': [
                {
                    'id': match.id,
                    'timestamp': match.timestamp,
                    'date': str(match.date),
                    'home_team_name': match.home_team_name,
                    'home_team_score': match.home_team_score,
                    'away_team_name': match.away_team_name,
                    'away_team_score': match.away_team_score,
                    'league_name': match.league_name,
                    'country': match.country,
                    'final_total_score': match.final_total_score,
                    'main_team': match.main_team,
                    'result_for_main_team': match.result_for_main_team,
                }
                for match in self.away_matches
            ],
            'head2heads_matches': [
                {
                    'id': match.id,
                    'timestamp': match.timestamp,
                    'date': str(match.date),
                    'home_team_name': match.home_team_name,
                    'home_team_score': match.home_team_score,
                    'away_team_name': match.away_team_name,
                    'away_team_score': match.away_team_score,
                    'league_name': match.league_name,
                    'country': match.country,
                    'final_total_score': match.final_total_score,
                    'main_team': match.main_team,
                    'result_for_main_team': match.result_for_main_team,
                }
                for match in self.head2head_matches
            ]
        }
