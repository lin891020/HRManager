from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.models import Employee, Base

# 定義資料庫 URL
DATABASE_URL = "sqlite:///./app/employees.db"  # 確保是相對路徑，讓它存在於 app/ 內

# 創建 SQLAlchemy 引擎
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

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
