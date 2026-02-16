from fastapi import FastAPI
from .api.health import router as health_router
from .api.inbox import router as inbox_router
from .api.drafts import router as drafts_router

app = FastAPI(title="HomeLedger", version="0.1.0")

app.include_router(health_router)
app.include_router(inbox_router)
app.include_router(drafts_router)
