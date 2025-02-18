from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

# 這個Repo裡寫的東西們
from database import get_session
from models import Restaurant, UpdateRestaurantRequest
from services.google_maps import search_nearby_restaurants, get_restaurant_info, get_restaurant_by_name

router = APIRouter()

# get all
@router.get("/")
# def list_restaurants(session: Session = Depends(get_session)):
#     restaurants = session.exec(select(Restaurant)).all()
#     return restaurants
# 取得所有餐廳資訊，可用 ?visited=false 篩選「還沒吃過」的餐廳
def get_restaurants(
    visited: Optional[bool] = Query(None, description="篩選是否已造訪（true 為已造訪，false 為未造訪）"),
    session: Session = Depends(get_session)
):
    query = select(Restaurant)
    if visited is not None:
        query = query.where(Restaurant.visited == visited)
    results = session.exec(query).all()
    return results


# 使用googlemaps 透過店名搜尋餐廳，並返回搜尋結果
@router.get("/find")
def search_restaurant_by_name(query: str = Query(..., description="餐廳名稱")):
    result = get_restaurant_by_name(query)
    return result

# 使用googlemaps 根據經緯度搜尋附近的餐廳   (lng:經度 lat:緯度)
@router.get("/search")
def search_restaurants(
    lat: float = Query(25.0330, ge=-90, le=90),  # 允許緯度範圍是 -90 到 90
    lng: float = Query(121.5654, ge=-180, le=180),  # 允許經度範圍是 -180 到 180
    radius: int = Query(1000, ge=0)  # 範圍最小值是 0
):
    print(f"Received lat: {lat}, lng: {lng}, radius: {radius}")
    data = search_nearby_restaurants(lat, lng, radius)
    results = []

    if "results" in data:
        for place in data["results"]:
            results.append({
                "name": place["name"],
                "address": place.get("vicinity", "未知地址"),
                "place_id": place["place_id"]
            })
    
    return results


# 使用googlemaps 查詢餐廳詳細資料
@router.get("/details")
def restaurant_details(place_id: str):
    details = get_restaurant_info(place_id)
    if "error" in details:
        return {"error": details["error"]}
    
    return details


# 新增餐廳到 ToEatList
@router.post("/add")
# def add_restaurant(name: str, address: str, session: Session = Depends(get_session)):
def add_restaurant(place_id: str, session: Session = Depends(get_session)):
    # new_restaurant = Restaurant(
    #     name=name,
    #     address=address,
    #     visited=False
    # )
    # session.add(new_restaurant)
    # session.commit()
    # session.refresh(new_restaurant)
    
    # return {"message": "餐廳已加入", "restaurant": new_restaurant}

    # 使用google maps取得餐廳地址

    # 使用 place_id 透過 Google Maps API 查詢餐廳詳細資料
    details = restaurant_details(place_id)
    if "error" in details:
        raise HTTPException(status_code=400, detail="無效的餐廳資訊")

    # 檢查資料庫是否已有相同的餐廳
    existing_restaurant = session.query(Restaurant).filter(Restaurant.name == details["name"]).first()
    if existing_restaurant:
        raise HTTPException(status_code=400, detail="餐廳已存在於清單中")

    # 新增餐廳
    new_restaurant = Restaurant(
        name=details["name"],
        address=details["address"],
        visited=False  # 預設狀態為尚未吃過
    )

    session.add(new_restaurant)
    session.commit()

    return {"message": "餐廳已成功加入", "restaurant": details}


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

