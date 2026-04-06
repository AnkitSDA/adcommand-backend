from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import dashboard, clients, alerts
import uvicorn

app = FastAPI(title="AdCommand API", version="1.0.0")

# Allow React frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","https://adcommand-frontend-4gmbygk9b-ankitsdas-projects.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routes
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(clients.router,   prefix="/api/clients",   tags=["Clients"])
app.include_router(alerts.router,    prefix="/api/alerts",    tags=["Alerts"])

@app.get("/")
def root():
    return {"status": "AdCommand API is running ✅", "version": "1.0.0"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)