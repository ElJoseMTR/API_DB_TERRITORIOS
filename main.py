from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import connect_db, close_connection
from routers import users, territorios, exhibidores


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.on_event("startup")
async def startup_db():
    connect_db()  

@app.on_event("shutdown")
async def shutdown_db():
    close_connection()  

# Routers
app.include_router(users.router)
app.include_router(territorios.router)
app.include_router(exhibidores.router)
