from fastapi import FastAPI
from fastapi_mcp import MPCApp
from fastapi_mcp import MPCConfig

app = FastAPI()
mpc_app = MPCApp(app)

@app.get("/")
async def root():
    return {"message": "MPC Party Ready"}
