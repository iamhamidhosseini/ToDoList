from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic
from app.db.session import db_session

T = TypeVar('T')

class BaseRepository(ABC, Generic[T]):
    def __init__(self):
        self.session = db_session.get_session()
    
    @abstractmethod
    def get_by_id(self, id: str) -> Optional[T]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[T]:
        pass
    
    @abstractmethod
    def create(self, entity: T) -> T:
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        pass
    
    @abstractmethod
    def delete(self, id: str) -> bool:
        pass
    
    def commit(self):
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
    
    def refresh(self, entity: T):
        self.session.refresh(entity)
