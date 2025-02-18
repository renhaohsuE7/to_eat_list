from sqlmodel import SQLModel, Session, create_engine

DATABASE_URL = "sqlite:///toeatlist.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


# 創建資料表（如果尚未創建）
def create_db_and_tables():
    SQLModel.metadata.create_all(bind=engine)


# 初始化資料庫的函式
def init_db():
    create_db_and_tables()

# 取得 Session
def get_session():
    with Session(engine) as session:
        yield session