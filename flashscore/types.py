from dataclasses import dataclass
from typing import List


@dataclass()
class Match:
    id: str

    
@dataclass()
class League:
    id: str
    name: str
    url: str
    api_endpoint: str

    
@dataclass()
class Country:
    id: int
    name: str
    url: str
    leagues: List[League]
