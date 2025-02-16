from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Optional

# SQLite 資料庫
DATABASE_URL = "sqlite:///./toeatlist.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 定義餐廳模型
class Restaurant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    address: str
    visited: bool = Field(default=False)

# 建立資料表
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# 取得資料庫 Session
def get_session():
    with Session(engine) as session:
        yield session
