# from fastapi import FastAPI, HTTPException, Query,Depends
# from contextlib import asynccontextmanager
# from sqlmodel import Session, select
# from typing import List, Optional

# from models import Restaurant, create_db_and_tables, get_session, engine

# # 設定 lifespan 事件處理器
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     print("📌 伺服器啟動，建立資料庫...")
#     create_db_and_tables()
#     yield  # 這裡是 "運行期間"
#     print("📌 伺服器關閉，釋放資源...")

# # 建立 FastAPI 應用
# app = FastAPI(lifespan=lifespan)

# 上面的是最開始的範例 之後修正

from fastapi import FastAPI
# from routers import restaurants, todo
from routers import restaurants
from database import init_db

app = FastAPI()

# 初始化資料庫
init_db()

# 載入 API 路由
app.include_router(restaurants.router, prefix="/restaurants", tags=["Restaurants"])
# app.include_router(todo.router, prefix="/todo", tags=["To-Do List"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)





# # # 🔹 1️⃣ 取得所有待吃餐廳
# # @app.get("/restaurants/", response_model=List[Restaurant])
# # def get_restaurants(session: Session = Depends(get_session)):
# #     restaurants = session.exec(select(Restaurant)).all()
# #     return restaurants

# # 取得資料庫 Session
# def get_session():
#     with Session(engine) as session:
#         yield session

# @app.get("/restaurants")
# def get_restaurants(visited: Optional[bool] = Query(None), session: Session = Depends(get_session)):
#     """
#     取得所有餐廳資訊，可用 `?visited=false` 來篩選「還沒吃過」的餐廳。
#     """
#     query = select(Restaurant)
    
#     # 如果請求有帶 `visited` 參數，則篩選
#     if visited is not None:
#         query = query.where(Restaurant.visited == visited)

#     results = session.exec(query).all()
#     return results


# # 🔹 2️⃣ 新增餐廳
# @app.post("/restaurants/", response_model=Restaurant)
# def add_restaurant(restaurant: Restaurant, session: Session = Depends(get_session)):
#     session.add(restaurant)
#     session.commit()
#     session.refresh(restaurant)
#     return restaurant

# # 🔹 3️⃣ 更新餐廳資訊
# @app.put("/restaurants/{restaurant_id}", response_model=Restaurant)
# def update_restaurant(restaurant_id: int, updated_restaurant: Restaurant, session: Session = Depends(get_session)):
#     restaurant = session.get(Restaurant, restaurant_id)
#     if not restaurant:
#         raise HTTPException(status_code=404, detail="找不到該餐廳")

#     restaurant.name = updated_restaurant.name
#     restaurant.address = updated_restaurant.address
#     restaurant.visited = updated_restaurant.visited

#     session.commit()
#     session.refresh(restaurant)
#     return restaurant

# # 🔹 4️⃣ 刪除餐廳
# @app.delete("/restaurants/{restaurant_id}")
# def delete_restaurant(restaurant_id: int, session: Session = Depends(get_session)):
#     restaurant = session.get(Restaurant, restaurant_id)
#     if not restaurant:
#         raise HTTPException(status_code=404, detail="找不到該餐廳")

#     session.delete(restaurant)
#     session.commit()
#     return {"message": f"已刪除 ID {restaurant_id} 的餐廳"}
