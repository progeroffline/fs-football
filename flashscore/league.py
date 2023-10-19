from typing import Optional
from .base import Base
from .season import Season


class League(Base):
    def __init__(self,
                 id: str,
                 name: str,
                 url: str,
                 country_id: int,
                 country_name: str,
                 api_endpoint: str,
                 locale: Optional[str] = 'en'):
        self.locale = locale
        super().__init__(self.locale)
        
        self.id = id
        self.name = name
        self.url = url
        self.country_id = country_id
        self.country_name = country_name
        self.api_endpoint = api_endpoint
        
    def __repr__(self) -> str:
        return "%s(id='%s', name='%s', url='%s')" % (
            self.__class__.__name__,
            self.id,
            self.name,
            self.url,
        )

    def get_seasons(self):
        """ Unfortunately only hardcoding """
        seasons_ids = [
            183, 176, 172, 171, 170, 169, 168, 167, 165, 160, 137, 81, 80, 64,
            5, 4, 11, 12, 13, 14, 15, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
            29, 30, 31, 32,
        ]
        
        seasons_titles = [
            "2023/2024", "2022/2023", "2021/2022", "2020/2021", "2019/2020",
            "2018/2019", "2017/2018", "2016/2017", "2015/2016", "2014/2015",
            "2013/2014", "2012/2013", "2011/2012", "2010/2011", "2009/2010",
            "2008/2009", "2007/2008", "2006/2007", "2005/2006", "2004/2005",
            "2003/2004", "2002/2003", "2001/2002", "2000/2001", "1999/2000",
            "1998/1999", "1997/1998", "1996/1997", "1995/1996", "1994/1995",
            "1993/1994", "1992/1993", "1991/1992", "1990/1991", "1989/1990",
        ]
        
        return [
            Season(
                id=id,
                title=title,
                country_id=self.country_id,
                league_id=self.id,
                country_name=self.country_name,
                league_name=self.name,
            )
            for id, title in zip(seasons_ids, seasons_titles)
        ]
