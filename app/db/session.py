from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config

class DatabaseSession:
    def __init__(self):
        self.database_url = Config.DATABASE_URL
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable is not set")
        
        # For SQLite, we need to add check_same_thread=False
        if self.database_url.startswith('sqlite'):
            self.engine = create_engine(self.database_url, connect_args={"check_same_thread": False})
        else:
            self.engine = create_engine(self.database_url)
            
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def get_session(self):
        return self.SessionLocal()
    
    def create_tables(self):
        from app.db.base import Base
        Base.metadata.create_all(bind=self.engine)

# Global database session instance
db_session = DatabaseSession()
