# AIzaSyCpP8c2OG0753l41i26x35s_JepFAtMrM0
import googlemaps

API_KEY = "AIzaSyCpP8c2OG0753l41i26x35s_JepFAtMrM0"
gmaps = googlemaps.Client(key=API_KEY)

def search_restaurants():
    location = (25.0330, 121.5654)  # 台北101 經緯度
    radius = 1000  # 搜尋半徑（公尺）
    
    results = gmaps.places_nearby(location=location, radius=radius, type="restaurant")["results"]

    for place in results[:5]:  # 只顯示前 5 筆
        name = place.get("name")
        rating = place.get("rating", "無評分")
        address = place.get("vicinity", "無地址")
        
        print(f"🏠 {name}")
        print(f"⭐ 評分: {rating}")
        print(f"📍 地址: {address}")
        print("-" * 40)

if __name__ == "__main__":
    search_restaurants()


# import googlemaps
# from datetime import datetime

# gmaps = googlemaps.Client(key='AIzaSyCpP8c2OG0753l41i26x35s_JepFAtMrM0')

# # Geocoding an address
# geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

# # Look up an address with reverse geocoding
# reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# # Request directions via public transit
# now = datetime.now()
# directions_result = gmaps.directions("Sydney Town Hall",
#                                      "Parramatta, NSW",
#                                      mode="transit",
#                                      departure_time=now)

# # Validate an address with address validation
# addressvalidation_result =  gmaps.addressvalidation(['1600 Amphitheatre Pk'], 
#                                                     regionCode='US',
#                                                     locality='Mountain View', 
#                                                     enableUspsCass=True)

# # Get an Address Descriptor of a location in the reverse geocoding response
# address_descriptor_result = gmaps.reverse_geocode((40.714224, -73.961452), enable_address_descriptor=True)
