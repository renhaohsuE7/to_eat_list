let map;
let markers = [];  // 用來儲存圖釘

// 初始化 Google 地圖
async function initMap() {
  const defaultLat = 25.0330;
  const defaultLng = 121.5654;
  
  // 建立地圖並將其放置在容器中
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: defaultLat, lng: defaultLng },
    zoom: 14,
  });

  // 當地圖初始化完成後，從後端取得餐廳資料
  try {
    console.log("從後端拿資料")
    const response = await fetch("http://127.0.0.1:8000/restaurants/");  // 假設你的後端路由是 /restaurants
    const restaurants = await response.json();

    // 清除舊的圖釘
    markers.forEach(marker => marker.setMap(null));
    markers = [];

    // 依據後端資料更新餐廳列表和 Google Map 圖釘
    updateRestaurantList(restaurants);
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

// 在地圖上加上餐廳的圖釘
function addMarkersToMap(restaurants) {
  restaurants.forEach(restaurant => {
    const marker = new google.maps.Marker({
      position: { lat: parseFloat(restaurant.latitude), lng: parseFloat(restaurant.longitude) },
      map: map,
      title: restaurant.name,
    });

    // 把標記儲存到 markers 陣列
    markers.push(marker);
  });
}

// 初始載入地圖
window.initMap = initMap;
