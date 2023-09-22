from .base import Base


class Match(Base):
    def __init__(self, id: str):
        super().__init__()
        
        self.id = id
