// 儲存餐廳資料
let restaurants = [];

// 這個方法會初始化Google地圖
function initMap() {
    const map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 25.0330, lng: 121.5654 }, // 預設位置，台北
        zoom: 14,
    });

    // 顯示餐廳標註
    for (const restaurant of restaurants) {
        const marker = new google.maps.Marker({
            position: { lat: restaurant.latitude, lng: restaurant.longitude },
            map: map,
            title: restaurant.name,
        });
    }
}

// 假資料，會從後端取得
function loadRestaurants() {
    // 這裡模擬後端資料
    setTimeout(() => {
        restaurants = [
            { name: "餐廳 A", address: "地址 A", latitude: 25.0330, longitude: 121.5654 },
            { name: "餐廳 B", address: "地址 B", latitude: 25.0360, longitude: 121.5674 },
            { name: "餐廳 C", address: "地址 C", latitude: 25.0400, longitude: 121.5700 },
        ];

        // 清空餐廳列表
        const list = document.getElementById("restaurantList");
        list.innerHTML = '';

        // 更新餐廳列表
        for (const restaurant of restaurants) {
            const li = document.createElement("li");
            li.textContent = `${restaurant.name} - ${restaurant.address}`;
            list.appendChild(li);
        }

        // 初始化地圖
        initMap();
    }, 2000); // 假資料延遲 2 秒
}

// 搜尋餐廳功能
function searchRestaurant() {
    const searchQuery = document.getElementById("searchInput").value.toLowerCase();
    const filteredRestaurants = restaurants.filter(restaurant => 
        restaurant.name.toLowerCase().includes(searchQuery) ||
        restaurant.address.toLowerCase().includes(searchQuery)
    );

    // 清空餐廳列表
    const list = document.getElementById("restaurantList");
    list.innerHTML = '';

    // 顯示篩選後的餐廳
    if (filteredRestaurants.length === 0) {
        const li = document.createElement("li");
        li.textContent = "無符合的餐廳";
        list.appendChild(li);
    } else {
        for (const restaurant of filteredRestaurants) {
            const li = document.createElement("li");
            li.textContent = `${restaurant.name} - ${restaurant.address}`;
            list.appendChild(li);
        }
    }
}

// 頁面載入時，呼叫 loadRestaurants 來初始化
window.onload = loadRestaurants;
