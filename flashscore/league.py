    
class League:
    def __init__(self, id: str, name: str, url: str, api_endpoint: str):
        self.id = id
        self.name = name
        self.url = url
        self.api_endpoint = api_endpoint

    def __repr__(self) -> str:
        return "%s(id='%s', name='%s')" % (
            self.__class__.__name__,
            self.id,
            self.name,
        )
