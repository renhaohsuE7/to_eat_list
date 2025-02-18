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

// // 在地圖上加上餐廳的圖釘 (使用 AdvancedMarkerElement)  但是怎樣都無法把店名放上去 擱置
// function addMarkersToMap(restaurants) {
//     console.log(restaurants);
//     const { AdvancedMarkerElement } = google.maps.marker; // 取得 AdvancedMarkerElement

//     restaurants.forEach(restaurant => {
//         const marker = new AdvancedMarkerElement({
//             position: new google.maps.LatLng(parseFloat(restaurant.latitude), parseFloat(restaurant.longitude)),
//             map: map,
//             title: restaurant.name,
//         });

//         // 使用 InfoWindow 顯示餐廳名稱和其他信息
//         const infoWindow = new google.maps.InfoWindow({
//             content: `<h3>${restaurant.name}</h3><p>${restaurant.address}</p>`
//         });

//         // 當使用者點擊圖釘時，顯示資訊視窗
//         marker.addListener('click', () => {
//             infoWindow.open(map, marker);
//         });

        
        
//         // // 自定義標籤顯示餐廳名稱
//         // const label = document.createElement('div');
//         // label.textContent = restaurant.name;
//         // label.style.fontSize = '14px';
//         // label.style.fontWeight = 'bold';
//         // label.style.backgroundColor = 'white';
//         // label.style.padding = '5px';
//         // label.style.borderRadius = '5px';
//         // label.style.boxShadow = '0 0 5px rgba(0,0,0,0.5)';
//         // label.style.textAlign = 'center';
//         // label.style.position = 'absolute';
//         // label.style.top = '-30px'; // 讓名稱顯示在圖釘上方
//         // label.style.left = '-50%';  // 居中顯示

//         // // 把自定義標籤加入地圖上的 marker
//         // marker.appendChild(label);
        

//         // 把標記儲存到 markers 陣列
//         markers.push(marker);
//     });
// }

// 在地圖上加上餐廳的圖釘 (使用 google.maps.Marker)
function addMarkersToMap(restaurants) {
    console.log(restaurants);

    restaurants.forEach(restaurant => {
        // 建立 google.maps.Marker
        const marker = new google.maps.Marker({
            position: new google.maps.LatLng(parseFloat(restaurant.latitude), parseFloat(restaurant.longitude)),
            map: map,
            title: restaurant.name,
            zIndex: 1   /// 還是改不了阿
        });

        // 建立資訊視窗
        const infoWindow = new google.maps.InfoWindow({
            content: `<h3>${restaurant.name}</h3><p>${restaurant.address}</p>`
        });

        // 當使用者點擊圖釘時，顯示資訊視窗
        marker.addListener('click', () => {
            infoWindow.open(map, marker);
        });

        // 顯示餐廳名稱 創建自訂的 DOM 元素並將其顯示
        const nameLabel = document.createElement('div');
        nameLabel.textContent = restaurant.name;
        nameLabel.style.position = 'absolute';
        nameLabel.style.fontSize = '12px';
        nameLabel.style.fontWeight = 'bold';
        nameLabel.style.color = '#333';
        nameLabel.style.backgroundColor = 'white';
        nameLabel.style.padding = '5px';
        nameLabel.style.borderRadius = '5px';
        nameLabel.style.boxShadow = '0 0 5px rgba(0,0,0,0.5)';
        nameLabel.style.zIndex = 100;    /// 還是改不了阿?!

        // 設定標籤位置
        const overlay = new google.maps.OverlayView();
        overlay.onAdd = function () {
            const panes = this.getPanes();
            panes.overlayLayer.appendChild(nameLabel);
        };
        overlay.draw = function () {
            const position = marker.getPosition(); // 這裡可以從 marker 獲得位置
            const projection = this.getProjection();
            const pixelPosition = projection.fromLatLngToDivPixel(position);
            nameLabel.style.left = `${pixelPosition.x - 20}px`;
            nameLabel.style.top = `${pixelPosition.y - 40}px`;             
            nameLabel.style.zIndex = 100
        };

        // 顯示標籤
        overlay.setMap(map);
    });
}



// 透過 onload 事件初始化地圖
window.onload = initMap;

document.addEventListener("DOMContentLoaded", () => {
    const addRestaurantBtn = document.getElementById("add-restaurant-btn");
    const placeIdInput = document.getElementById("place-id-input");

    // addRestaurantBtn.addEventListener("click", async () => {
    //     const placeId = placeIdInput.value.trim();
    //     if (!placeId) {
    //         alert("請輸入 Google Place ID！");
    //         return;
    //     }

    //     try {
    //         const response = await fetch("http://127.0.0.1:8000/restaurants/add", {
    //             method: "POST",
    //             headers: {
    //                 "Content-Type": "application/json",
    //             },
    //             body: JSON.stringify({ place_id: placeId }),
    //         });

    //         const data = await response.json();
    //         if (response.ok) {
    //             alert("餐廳已成功加入！");
    //             placeIdInput.value = ""; // 清空輸入框
    //             fetchRestaurantData(); // 重新取得餐廳列表，更新畫面
    //         } else {
    //             alert("錯誤：" + data.detail);
    //         }
    //     } catch (error) {
    //         console.error("Error adding restaurant:", error);
    //         alert("無法加入餐廳，請稍後再試！");
    //     }
    // });
});


// 搜尋餐廳功能
async function searchRestaurant() {
    const restaurantName = document.getElementById("restaurant-search").value;

    if (!restaurantName) {
        alert("請輸入餐廳名稱");
        return;
    }

    try {
        // 向後端請求餐廳搜尋結果，改用 query 參數
        const response = await fetch(`http://127.0.0.1:8000/restaurants/find?query=${restaurantName}`);
        const data = await response.json();
        console.log(data)
        // 檢查返回的資料是否為陣列
        if (Array.isArray(data)) {
            // 顯示搜尋結果
            displaySearchResults(data);
        } else {
            // 若返回錯誤訊息，顯示錯誤
            alert("找不到相關餐廳");
        }
    } catch (error) {
        console.error("Error searching restaurant:", error);
    }
}

// 顯示搜尋結果
function displaySearchResults(restaurants) {
    const resultsContainer = document.getElementById("search-results");
    resultsContainer.innerHTML = '';  // 清空現有的搜尋結果

    if (restaurants.length === 0) {
        resultsContainer.innerHTML = '找不到相關餐廳';
        return;
    }

    restaurants.forEach(restaurant => {
        const resultItem = document.createElement("div");
        resultItem.classList.add("search-result-item");

        const name = document.createElement("span");
        name.textContent = restaurant.name;

        const addButton = document.createElement("button");
        addButton.textContent = "加入餐廳";
        addButton.onclick = () => addRestaurantToList(restaurant.place_id);

        resultItem.appendChild(name);
        resultItem.appendChild(addButton);

        resultsContainer.appendChild(resultItem);
    });
}

// 新增餐廳到清單
async function addRestaurantToList(place_id) {
    try {
        const response = await fetch("http://127.0.0.1:8000/restaurants/add", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ place_id: place_id })
        });

        const data = await response.json();

        if (data.message) {
            alert(data.message);
        }

        // 可以在這裡更新餐廳清單
        fetchRestaurantData();  // 重新載入餐廳清單
    } catch (error) {
        console.error("Error adding restaurant:", error);
    }
}
