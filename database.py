from sqlmodel import SQLModel, Session, create_engine
# from models.models import Restaurant

DATABASE_URL = "sqlite:///toeatlist.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 初始化資料庫
def init_db():
    SQLModel.metadata.create_all(engine)

# 取得 Session
def get_session():
    with Session(engine) as session:
        yield session