from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from routers import auth_routes, document_routes, passport_routes, dashboard_routes

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Huella API",
    description="Sustainability Passport & Carbon Tracking API",
    version="1.0.0"
)

# CORS Middleware for Frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth_routes.router)
app.include_router(document_routes.router)
app.include_router(passport_routes.router)
app.include_router(dashboard_routes.router)

@app.get("/")
def root():
    return {
        "app": "Huella API",
        "status": "online",
        "documentation": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
