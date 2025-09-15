from fastapi import FastAPI
from routes.profile import router as profiles_router
from routes.transaction import router as transaction_router

app = FastAPI(title="Agri Supply Chain API")

# Include router
app.include_router(profiles_router)
app.include_router(transaction_router)


@app.get("/")
def root():
    return {"msg": "Welcome to Agri Supply Chain API"}
