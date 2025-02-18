import googlemaps
from fastapi import HTTPException
from typing import List, Dict
from config import settings

from models import Restaurant

gmaps = googlemaps.Client(key=settings.google_maps_api_key)

# 使用 Google Maps API 搜尋附近的餐廳 並以中文回傳結果
def search_nearby_restaurants(lat: float, lng: float, radius: int = 1000) -> Dict:
    places = gmaps.places_nearby(
        location=(lat, lng),
        radius=radius,
        type="restaurant",
        language="zh-TW" 
    )
    
    if places.get("status") == "OK":
        return places
    else:
        return {"error": "無法搜尋餐廳"}

# 根據餐廳的 place_id 獲取詳細資料 （以中文回傳）
def get_place_details(place_id: str) -> Dict:
    place = gmaps.place(place_id, language="zh-TW")
    
    if place.get("status") == "OK":
        return place
    else:
        return {"error": "無法獲取餐廳詳細資訊"}

# 綜合查詢餐廳的基本資訊，包含: 名稱, 地址, 經度, 緯度, place_id, (以後增加菜單或最新評論等等)
def get_restaurant_info(place_id: str) -> Dict:
    details = get_place_details(place_id)
    
    if "result" in details:
        result = details["result"]
        
        return {
            "name": result["name"],
            "address": result["formatted_address"],
            "latitude": result["geometry"]["location"]["lat"],  # 新增經度
            "longitude": result["geometry"]["location"]["lng"],  # 新增緯度
            "place_id": place_id  # 直接使用傳入的 place_id
        }
    
    return {"error": "餐廳資訊無效"}

# 使用 Google Maps API 以店名搜尋餐廳
def find_place_by_name(query: str) -> Dict:
    result = gmaps.find_place(
        input=query,
        input_type="textquery",
        fields=["place_id", "name", "formatted_address"],
        language="zh-TW"
    )
    return result

# 擷取第一筆結果
def get_restaurant_by_name(query: str) -> Dict:
    result = find_place_by_name(query)
    if result.get("status") == "OK" and result.get("candidates"):
        candidate = result["candidates"][0]
        return {
            "place_id": candidate.get("place_id"),
            "name": candidate.get("name"),
            "address": candidate.get("formatted_address")
        }
    else:
        return {"error": "找不到符合的餐廳"}



# 使用 Google Maps Places API 搜尋餐廳
def search_restaurant_by_google(query: str) -> List[Restaurant]:
    # 使用 Google Maps Places API 進行文字搜尋
    places_result = gmaps.places(query + " restaurant", language='zh-TW')  # 這會搜尋包含 'restaurant' 關鍵字的地方

    if 'results' not in places_result:
        raise HTTPException(status_code=404, detail="未找到相關餐廳")

    # 把搜尋結果轉換成餐廳模型的列表
    restaurants = []
    for place in places_result['results']:
        restaurant = Restaurant(
            name=place['name'],
            address=place.get('formatted_address', 'N/A'),
            latitude=place['geometry']['location']['lat'],
            longitude=place['geometry']['location']['lng'],
            place_id=place['place_id']
        )
        restaurants.append(restaurant)

    return restaurants