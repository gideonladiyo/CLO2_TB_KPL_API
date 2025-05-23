from fastapi import FastAPI
from routers import gacha, user, banner

app = FastAPI(
    title="Studi Kasus FastAPI - Dua Group Service",
    description="API untuk mengelola data produk dan pelanggan.",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "User",
            "description": "user endpoint",
        },
        {
            "name": "Gacha",
            "description": "gacha endpoint",
        },
        {
            "name": "Banner",
            "description": "banner endpoint"
        }
    ],
)

# Daftarkan router
app.include_router(user.router)
app.include_router(gacha.router)
app.include_router(banner.router)