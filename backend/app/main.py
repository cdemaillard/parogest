from fastapi import FastAPI
from datetime import datetime
from app.routes import suppliers, contacts, categories, users, expenses

app = FastAPI(
  title="ParoGest API",
  description="API de gestion comptable pour les paroisses",
  version="0.1.0"
)

app.include_router(contacts.router)
app.include_router(suppliers.router)
app.include_router(categories.router)
app.include_router(users.router)
app.include_router(expenses.router)

@app.get("/")
def root():
  return {
    "app": "ParoGest API",
    "version": "0.2.0",
    "status" : "running",
    "timestamp": datetime.now().isoformat()
  }

@app.get("/health")
def health_check():
  return {"status": "healthy"}