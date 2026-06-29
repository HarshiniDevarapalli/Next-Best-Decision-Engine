from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from api.routes import router


app = FastAPI(
    title="Next Best Decision Engine",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Next Best Decision Engine API is running."
    }
