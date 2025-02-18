import googlemaps
from typing import List, Dict
from config import settings

API_KEY = "AIzaSyCpP8c2OG0753l41i26x35s_JepFAtMrM0"

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

# 綜合查詢餐廳的基本資訊，包含名稱和地址
def get_restaurant_info(place_id: str) -> Dict:
    details = get_place_details(place_id)
    if "result" in details:
        return {
            "name": details["result"]["name"],
            "address": details["result"]["formatted_address"]
        }
    else:
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
