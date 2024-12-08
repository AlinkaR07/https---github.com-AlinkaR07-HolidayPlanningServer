from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Настройка подключения к PostgreSQL
DATABASE_URL = "postgresql://postgres:051023@localhost:5432/holidayplanning_bd"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()