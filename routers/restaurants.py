from fastapi import APIRouter, Depends, HTTPException
# from services.google_maps import search_nearby_restaurants, get_place_details
from database import get_session
from sqlmodel import Session, select
from models import Restaurant, UpdateRestaurantRequest

router = APIRouter()

# get all
@router.get("/")
def list_restaurants(session: Session = Depends(get_session)):
    restaurants = session.exec(select(Restaurant)).all()
    return restaurants


# 新增餐廳到 ToEatList
@router.post("/add")
def add_restaurant(name: str, address: str, session: Session = Depends(get_session)):
    new_restaurant = Restaurant(
        name=name,
        address=address,
        visited=False
    )
    session.add(new_restaurant)
    session.commit()
    session.refresh(new_restaurant)
    
    return {"message": "餐廳已加入", "restaurant": new_restaurant}


# 根據 ID 查詢餐廳
@router.get("/{restaurant_id}")
def get_restaurant(restaurant_id: int, session: Session = Depends(get_session)):
    restaurant = session.get(Restaurant, restaurant_id)
    if not restaurant:
        return {"error": "找不到該餐廳"}
    return restaurant


# 更新餐廳的狀態（標記為已造訪）
@router.put("/{restaurant_id}")
def update_restaurant(restaurant_id: int, data: UpdateRestaurantRequest, session: Session = Depends(get_session)):

    # try:
    #     print("Received data:", data)
    # except Exception as e:
    #     raise HTTPException(status_code=400, detail=str(e))

    restaurant = session.get(Restaurant, restaurant_id)
    if not restaurant:
        return {"error": "找不到該餐廳"}

    # 更新餐廳的 visited 狀態
    restaurant.visited = data.visited
    session.add(restaurant)
    session.commit()
    return {"message": "更新成功", "restaurant": restaurant}



@router.delete("/{restaurant_id}")
def delete_restaurant(restaurant_id: int, session: Session = Depends(get_session)):
    """
    刪除餐廳
    """
    restaurant = session.get(Restaurant, restaurant_id)
    if not restaurant:
        return {"error": "找不到該餐廳"}

    session.delete(restaurant)
    session.commit()
    return {"message": "刪除成功"}
