from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import restaurants, googlemaps_router  
from database import init_db
from contextlib import asynccontextmanager

# 設定 lifespan 事件處理器
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("📌 伺服器啟動，建立資料庫...")
    init_db()  # 在這裡初始化資料庫
    yield  # 這裡是 "運行期間"
    print("📌 伺服器關閉，釋放資源...")

app = FastAPI(lifespan=lifespan)

# 只允許特定的來源的請求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # 允許來自前端的來源
    allow_credentials=True,
    allow_methods=["*"],  # 允許所有方法
    allow_headers=["*"],  # 允許所有標頭
)

# 載入 API 路由
app.include_router(restaurants.router, prefix="/restaurants", tags=["Restaurants"])
app.include_router(googlemaps_router.router, prefix="/googlemaps_router", tags=["Google Maps"])

# 啟動服務
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
