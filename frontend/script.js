let map;
let markers = [];  // 用來儲存圖釘
let isGoogleMapsLoaded = false; // 確保 Google Maps API 只載入一次

// 初始化 Google 地圖
async function initMap() {
    try {
        // 檢查是否已經加載過 Google Maps API
        if (isGoogleMapsLoaded) {
            console.log("Google Maps 已經加載過了，不再重複加載");
            return;  // 如果已經加載過，就不要重複執行
        }

        // 向後端請求 Google Maps API 金鑰
        const response = await fetch("http://127.0.0.1:8000/googlemaps_router/get-google-maps-api-key");
        const data = await response.json();
        const googleMapsApiKey = data.google_maps_api_key;
    
        // 動態加載 Google Maps API，並指定回調函數
        const script = document.createElement("script");
        script.src = `https://maps.googleapis.com/maps/api/js?key=${googleMapsApiKey}&callback=initializeMap&libraries=marker`;
        script.async = true;
        script.defer = true;
        document.head.appendChild(script);

        isGoogleMapsLoaded = true;  // 紀錄已經載入過
    } catch (error) {
        console.error("Error fetching Google Maps API key:", error);
    }
}

// 初始化地圖
function initializeMap() {
    const defaultLat = 25.0330;
    const defaultLng = 121.5654;

    // 建立地圖並將其放置在容器中
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: defaultLat, lng: defaultLng },
        zoom: 14,
        mapId: "ead5d021cf2571aa", // 為了使用 advance marker圖釘功能才加上這個 (是在googlemap服務頁面設定的)
    });

    // 取得餐廳資料
    fetchRestaurantData();
}

// 從後端取得餐廳資料
async function fetchRestaurantData() {
    try {
        console.log("從後端拿資料")
        const response = await fetch("http://127.0.0.1:8000/restaurants/");  // 假設你的後端路由是 /restaurants
        const restaurants = await response.json();

        // 清除舊的圖釘
        markers.forEach(marker => marker.setMap(null));
        markers = [];

        // 依據後端資料更新餐廳列表和 Google Map 圖釘
        updateRestaurantList(restaurants);
        console.log("準備新增圖釘")
        addMarkersToMap(restaurants);
    } catch (error) {
        console.error("Error fetching restaurant data:", error);
    }
}

// 更新頁面上的餐廳列表
function updateRestaurantList(restaurants) {
    const listContainer = document.getElementById("restaurant-list");
    listContainer.innerHTML = '';  // 清空現有的列表

    restaurants.forEach(restaurant => {
        const listItem = document.createElement("li");
        listItem.textContent = `${restaurant.name} - ${restaurant.address}`;
        listContainer.appendChild(listItem);
    });
}

// 在地圖上加上餐廳的圖釘 (使用 AdvancedMarkerElement)
function addMarkersToMap(restaurants) {
    console.log(restaurants)
    const { AdvancedMarkerElement } = google.maps.marker; // 取得 AdvancedMarkerElement

    restaurants.forEach(restaurant => {
        const marker = new AdvancedMarkerElement({
            position: new google.maps.LatLng(parseFloat(restaurant.latitude), parseFloat(restaurant.longitude)),
            map: map,
            title: restaurant.name,
        });

        // 把標記儲存到 markers 陣列
        markers.push(marker);
    });
}


// 透過 onload 事件初始化地圖
window.onload = initMap;
