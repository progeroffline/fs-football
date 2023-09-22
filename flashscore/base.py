import requests


class Base:
    def __init__(self):
        self.main_url = 'https://flashscore.com/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0',
            'Accept': '*/*',
            'Accept-Language': 'en',
            'Referer': 'https://www.flashscore.com/',
            'x-fsign': 'SW9D1eZo',
            'Origin': 'https://www.flashscore.com',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }
    
    def make_request(self, url: str) -> requests.Response:
        return requests.get(url, headers=self.headers) 
