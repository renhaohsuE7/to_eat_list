from sqlmodel import SQLModel, Field
from typing import Optional
# from pydantic import BaseModel, conbool

# 定義餐廳模型
class Restaurant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    address: str
    visited: bool = Field(default=False)  # 是否已經吃過

# 更新 "有沒有吃過這間餐廳"
class UpdateRestaurantRequest(SQLModel):
    # visited: bool
    visited: bool = Field(default=False)  # 是否已經吃過
