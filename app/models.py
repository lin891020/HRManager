from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://Mike:1020@hrmanager-db-1:5432/hrmanager"


# 建立資料庫連接引擎
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 定義 ORM 基礎類
Base = declarative_base()

# 定義員工資料表
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)  # 員工 ID
    name = Column(String, index=True)                  # 員工姓名
    age = Column(Integer)                              # 員工年齡
    position = Column(String)                          # 員工職位
    salary = Column(Float)                             # 員工薪資

# 建立 Session 類別
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
