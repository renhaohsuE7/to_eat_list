from fastapi import FastAPI, HTTPException, Depends
from contextlib import asynccontextmanager
from sqlmodel import Session, select
from typing import List

from models import Restaurant, create_db_and_tables, get_session

# 設定 lifespan 事件處理器
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("📌 伺服器啟動，建立資料庫...")
    create_db_and_tables()
    yield  # 這裡是 "運行期間"
    print("📌 伺服器關閉，釋放資源...")

# 建立 FastAPI 應用
app = FastAPI(lifespan=lifespan)

# 🔹 1️⃣ 取得所有待吃餐廳
@app.get("/restaurants/", response_model=List[Restaurant])
def get_restaurants(session: Session = Depends(get_session)):
    restaurants = session.exec(select(Restaurant)).all()
    return restaurants

# 🔹 2️⃣ 新增餐廳
@app.post("/restaurants/", response_model=Restaurant)
def add_restaurant(restaurant: Restaurant, session: Session = Depends(get_session)):
    session.add(restaurant)
    session.commit()
    session.refresh(restaurant)
    return restaurant

# 🔹 3️⃣ 更新餐廳資訊
@app.put("/restaurants/{restaurant_id}", response_model=Restaurant)
def update_restaurant(restaurant_id: int, updated_restaurant: Restaurant, session: Session = Depends(get_session)):
    restaurant = session.get(Restaurant, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="找不到該餐廳")

    restaurant.name = updated_restaurant.name
    restaurant.address = updated_restaurant.address
    restaurant.visited = updated_restaurant.visited

    session.commit()
    session.refresh(restaurant)
    return restaurant

# 🔹 4️⃣ 刪除餐廳
@app.delete("/restaurants/{restaurant_id}")
def delete_restaurant(restaurant_id: int, session: Session = Depends(get_session)):
    restaurant = session.get(Restaurant, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="找不到該餐廳")

    session.delete(restaurant)
    session.commit()
    return {"message": f"已刪除 ID {restaurant_id} 的餐廳"}
