# FlashScore Football Library

## Overview

This Python library allows you to easily scrape football match data from the FlashScore website (flashscore.com). It is designed to work asynchronously, ensuring fast and efficient data retrieval. In some parts of the library, it utilizes the `grequests` library for improved performance.

## Features

- Asynchronous data retrieval: The library leverages Python's `asyncio` framework to make asynchronous HTTP requests, enabling you to fetch data from FlashScore efficiently.

- Historical match data: Access historical data for past football matches, including match results, team statistics, and goal scorers..

## Installation

You can install the library via pip:

```shell
git clone ...
cd ...
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## Usage

Here's a simple example of how to use the library to retrieve history match data:

```python
from flashscore import FlashscoreApi

api = FlashscoreApi()
countries = api.get_countries()

for country in countries:
    leagues = country.get_leagues()

    for leauge in leagues:
        season = league.get_season()

        current_season = season[0]
        for match in current_season.get_matches():
            print(match)
            match.load_content()
            print(match)
```


Here's a simple example of how to use the library to retrieve today match data:

```python
from flashscore import FlashscoreApi

api = FlashscoreApi()
today_matches = api.get_today_matches()

for i, match in enumerate(today_matches):
    match.load_content()
```
## Author

- GitHub: [progeroffline](https://github.com/progeroffline)

If you have any questions or encounter any issues, please don't hesitate to open an issue on GitHub.

Happy scraping! 🚀📈
