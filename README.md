# to_eat_list


## notes:

venv:
```cmd
venv\Scripts\activate
```

run dev:
```cmd
fastapi dev main.py
```

## API功能說明

1. ToEatList API
- 新增 餐廳
- 取得 所有餐廳
- 更新 餐廳資訊（名稱、是否已吃過）
- 刪除 餐廳
- 餐廳包含資訊：id、名稱（name）、地址（address）、是否已吃過（visited）






## 一些openai給的提議

記錄一下問chatgpt時他給多額外資訊 
(未實際找文件來確認or測試)

### 分享資料庫結構

如果專案需要分享資料庫結構？
如果你的團隊或其他開發者也需要這個資料庫的表結構，但不需要你的測試數據，你可以：

提供 SQL Schema：

```sh
sqlite3 toeatlist.db .schema > schema.sql
```

然後提交 schema.sql，這樣團隊成員可以用：

```sh
sqlite3 toeatlist.db < schema.sql
```

來建立相同的表結構。

使用 SQLModel 自動生成表格 只提交程式碼，讓 FastAPI 在啟動時自動建立 SQLite 資料庫：

```python
from sqlmodel import SQLModel, create_engine

engine = create_engine("sqlite:///toeatlist.db")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
```