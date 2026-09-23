from sqlalchemy import create_engine, Column, String, Float, Integer
from sqlalchemy.orm import sessionmaker, scoped_session

# Database connection setup
DATABASE_URL = "sqlite:///./cargo.db"
# connects SQLAlchemy to the cargo.db SQLite database file
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# establishes database sessions, ensuring that each request uses its own connection to the database 
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

print("test")

