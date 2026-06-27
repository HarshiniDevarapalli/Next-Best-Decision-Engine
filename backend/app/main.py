from fastapi import FastAPI

from api.routes import router

app = FastAPI(
    title="Next Best Decision Engine",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
def root():
    return {
        "message": "Next Best Decision Engine API is running."
    }