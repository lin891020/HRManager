import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.models import Employee, Base

# 讀取環境變數
POSTGRES_USER = os.getenv("POSTGRES_USER", "Mike")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "1020")
POSTGRES_DB = os.getenv("POSTGRES_DB", "hrmanager")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "hrmanager-db-1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

# 設定 PostgreSQL 連接 URL
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# 創建 SQLAlchemy 引擎
engine = create_engine(DATABASE_URL)

# 創建 Session 類別
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 初始化資料庫（如果表格不存在則創建）
def init_db():
    Base.metadata.create_all(bind=engine)

# 取得資料庫 Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
