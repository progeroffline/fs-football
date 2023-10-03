# FlashScore Football Library

## Table of Contents

- [🌐 Languages](#languages)
- [📖 Overview](#overview)
- [🚀 Features](#features)
- [🛠 Installation](#installation)
- [🔍 Usage](#usage)
- [⚙️ Available Classes](#available-classes)
  - [StatValue](#statvalue)
  - [Odds](#odds)
  - [Event](#event)
  - [HistoryMatch](#historymatch)
  - [Match](#match)
- [👤 Author](#author)

## Languages

- [🇺🇸 English](README.md)
- [🇺🇦 Ukrainian](README-ua.md)

## Overview

This Python library allows you to easily fetch data about football matches from the FlashScore website (flashscore.com). It is designed for asynchronous operation, providing fast and efficient data retrieval. In some parts of the library, the `grequests` library is used to enhance performance.

## Features

- Asynchronous Data Retrieval: The library employs Python's asynchronous approach using the `asyncio` framework to make asynchronous HTTP requests, allowing for efficient data retrieval from FlashScore.

- Historical Match Data: Access to historical data about past football matches, including match results, team statistics, and top scorers.

## Installation

```shell
git clone https://github.com/progeroffline/fs-football-lib
cd fs-football-lib
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## Usage

Here is a simple example of using the library to fetch historical match data:

```python
from flashscore import FlashscoreApi

api = FlashscoreApi()
countries = api.get_countries()

for country in countries:
    leagues = country.get_leagues()

    for league in leagues:
        season = league.get_season()

        current_season = season[0]
        for match in current_season.get_matches():
            print(match)
            match.load_content()
            print(match)
```

Here is a simple example of using the library to fetch data about today's matches:

```python
from flashscore import FlashscoreApi

api = FlashscoreApi()
today_matches = api.get_today_matches()

for i, match in enumerate(today_matches):
    match.load_content()
```

## Available Classes

### StatValue 
Represents a statistical value in a match.
  - `name`: The name of the statistical value.
  - `home`: The value for the home team.
  - `away`: The value for the away team.

### Odds
Represents odds for a team.
  - `team`: The name of the team.
  - `value`: The odds value.

### Event
Represents an event in a match, such as a goal or a card.
  - `type`: The event type.
  - `player_name`: The name of the player involved in the event.
  - `player_url`: The URL associated with the player.
  - `time`: The time when the event occurred (optional).
  - `current_score`: The current score of the match (optional).
  - `second_player_name`: The name of the second player involved in the event (optional).
  - `second_player_url`: The URL associated with the second player (optional).
  - `description`: Additional description of the event (optional).

### HistoryMatch
Represents a historical match.
  - `id`: The unique identifier of the match.
  - `timestamp`: The timestamp of the match.
  - `date`: The date and time of the match.
  - `home_team_name`: The name of the home team.
  - `home_team_score`: The score of the home team.
  - `away_team_name`: The name of the away team.
  - `away_team_score`: The score of the away team.
  - `league_name`: The name of the league to which the match belongs.
  - `country`: The country in which the match took place.
  - `final_total_score`: The final total score of the match.
  - `main_team`: The main team in the match (optional).
  - `result_for_main_team`: The result for the main team (optional).

### Match
Represents a match, including its details and statistics.
  - `id`: The unique identifier of the match.
  - `country_name`: The name of the country where the match took place (optional).
  - `league_name`: The name of the league to which the match belongs (optional).
  - `timestamp`: The timestamp of the match (optional).
  - `date`: The date and time of the match (optional).
  - `tournament`: The name of the tournament (optional).
  - `home_team_name`: The name of the home team (optional).
  - `away_team_name`: The name of the away team (optional).
  - `home_team_score`: The score of the home team (optional).
  - `away_team_score`: The score of the away team (optional).
  - `final_total_score`: The final total score of the match (optional).
  - `status`: The match status (optional).
  - `stats_match`: A list of statistical values for the entire match.
  - `stats_first_half`: A list of statistical values for the first half.
  - `stats_second_half`: A list of statistical values for the second half.
  - `prematch_home_odds`: Odds for the home team before the match (optional).
  - `prematch_middle_odds`: Average odds before the match (optional).
  - `prematch_away_odds`: Odds for the away team before the match (optional).
  - `events`: A list of events that occurred during the match.
  - `home_matches`: A list of historical matches for the home team.
  - `away_matches`: A list of historical matches for the away team.
  - `head2head_matches`: A list of historical matches between these two teams.

## Author

- GitHub: [progeroffline](https://github.com/progeroffline)

If you have any questions or issues, please feel free to open GitHub issues.

Happy parsing! 🚀📈
