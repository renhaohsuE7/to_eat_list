from sqlmodel import SQLModel, Field
from typing import Optional
# from pydantic import BaseModel, conbool

# 定義餐廳模型
class Restaurant(SQLModel, table=True):
    # id: int = Field(default=None, primary_key=True)
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    address: str
    latitude: float  # 新增經度欄位
    longitude: float  # 新增緯度欄位
    place_id: str  # 新增 Google Maps place_id 欄位
    visited: bool = Field(default=False)

# 更新 "有沒有吃過這間餐廳"
class UpdateRestaurantRequest(SQLModel):
    # visited: bool
    visited: bool = Field(default=False)  # 是否已經吃過
