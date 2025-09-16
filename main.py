from fastapi import FastAPI, Request
from routes.profile import router as profiles_router
from routes.transaction import router as transaction_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Agri Supply Chain API",host="0.0.0.0")

# Include router
app.include_router(profiles_router)
app.include_router(transaction_router)


@app.get("/")
def root():
    return {"msg": "Welcome to Agri Supply Chain API"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)