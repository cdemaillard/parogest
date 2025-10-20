from fastapi import FastAPI
from datetime import datetime
from app.routes import suppliers

app = FastAPI(
  title="ParoGest API",
  description="API de gestion comptable pour les paroisses",
  version="0.1.0"
)

app.include_router(suppliers.router)

@app.get("/")
def root():
  return {
    "app": "ParoGest API",
    "version": "0.1.0",
    "status" : "running",
    "timestamp": datetime.now().isoformat()
  }

@app.get("/health")
def health_check():
  return {"status": "healthy"}