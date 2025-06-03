from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
<<<<<<< HEAD
=======
from .api.routes import api_router
from .models import base, books, users, loans  # Importer les modèles pour Alembic
>>>>>>> e755f60eb1799c1a84315aae1c917c71281c6e90

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configuration CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

<<<<<<< HEAD
=======
# Inclusion des routes API
app.include_router(api_router, prefix=settings.API_V1_STR)

>>>>>>> e755f60eb1799c1a84315aae1c917c71281c6e90
@app.get("/")
def read_root():
    return {"message": "Welcome to the Library Management System API"}