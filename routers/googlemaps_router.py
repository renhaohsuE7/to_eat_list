from fastapi import APIRouter, Query
from services.google_maps import search_nearby_restaurants
from config import settings

router = APIRouter()

# 注意: 這是googlemaps服務的特性 只能依靠在googlemaps的官網設定那邊進行限制
# 提供 Google Maps API 金鑰給前端 
# 雖然還是暴露到前端了 但沒關係 只要googlemaps服務有設定即可 (目前還沒)
@router.get("/get-google-maps-api-key")
async def get_google_maps_api_key():
    return {"google_maps_api_key": settings.google_maps_api_key}

@router.get("/search")
async def search_restaurants(lat: float, lng: float, radius: int = 1000):
    api_key = settings.google_maps_api_key  # 使用 Pydantic 來取得金鑰
    return search_nearby_restaurants(lat, lng, radius, api_key)
