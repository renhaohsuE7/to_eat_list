from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# 模擬資料庫
to_eat_list = []
restaurant_id_counter = 1  # 自動遞增 ID

# 定義餐廳資料結構
class Restaurant(BaseModel):
    id: int
    name: str
    address: str
    visited: bool = False

# 🔹 1️⃣ 取得所有待吃餐廳
@app.get("/restaurants/", response_model=List[Restaurant])
def get_restaurants():
    return to_eat_list

# 🔹 2️⃣ 新增餐廳
@app.post("/restaurants/", response_model=Restaurant)
def add_restaurant(restaurant: Restaurant):
    global restaurant_id_counter
    restaurant.id = restaurant_id_counter
    restaurant_id_counter += 1
    to_eat_list.append(restaurant)
    return restaurant

# 🔹 3️⃣ 更新餐廳資訊
@app.put("/restaurants/{restaurant_id}", response_model=Restaurant)
def update_restaurant(restaurant_id: int, updated_restaurant: Restaurant):
    for index, restaurant in enumerate(to_eat_list):
        if restaurant.id == restaurant_id:
            to_eat_list[index] = updated_restaurant
            return updated_restaurant
    raise HTTPException(status_code=404, detail="找不到該餐廳")

# 🔹 4️⃣ 刪除餐廳
@app.delete("/restaurants/{restaurant_id}")
def delete_restaurant(restaurant_id: int):
    global to_eat_list
    to_eat_list = [restaurant for restaurant in to_eat_list if restaurant.id != restaurant_id]
    return {"message": f"已刪除 ID {restaurant_id} 的餐廳"}
