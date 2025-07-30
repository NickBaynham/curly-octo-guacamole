# app/main.py
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from tests.playwright_runner import run_test
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Playwright Test API")

# ——— Demo models —————————————————————————————————————————————————————

class CreateAccountReq(BaseModel):
    expired_at: str        # e.g. "20250819"
    ui_test: bool = False  # Set to True to run UI tests

class CreateUserReq(BaseModel):
    action: str            # e.g. "create_user"
    ui_test: bool = False  # Set to True to run UI tests
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    gender: str
    birth: str             # YYYYMMDD
    agreed_terms: bool
    salary: int
    id: str

# ——— Endpoints ————————————————————————————————————————————————————————

@app.post("/create_account")
def create_account(req: CreateAccountReq):
    # Log the request details
    logger.info("=" * 60)
    logger.info("🚀 API REQUEST RECEIVED")
    logger.info("=" * 60)
    logger.info(f"📡 Endpoint: POST /create_account")
    logger.info(f"🔑 Keyword: create_account")
    logger.info(f"📊 Test Data: {req.model_dump()}")
    logger.info("-" * 60)
    
    # translate Pydantic model to dict
    result = run_test("create_account", req.model_dump())
    return {"status": "ok", "result": result}

@app.post("/create_user")
def create_user(req: CreateUserReq):
    # Log the request details
    logger.info("=" * 60)
    logger.info("🚀 API REQUEST RECEIVED")
    logger.info("=" * 60)
    logger.info(f"📡 Endpoint: POST /create_user")
    logger.info(f"🔑 Keyword: {req.action}")
    logger.info(f"📊 Test Data: {req.model_dump()}")
    logger.info(f"🖥️  UI Test: {req.ui_test}")
    logger.info("-" * 60)
    
    result = run_test(req.action, req.model_dump())
    return {"status": "ok", "result": result}

# Optional: generic endpoint for any test keyword
class GenericReq(BaseModel):
    keyword: str
    payload: dict

@app.post("/run_test")
def run_generic_test(req: GenericReq):
    # Log the request details
    logger.info("=" * 60)
    logger.info("🚀 API REQUEST RECEIVED")
    logger.info("=" * 60)
    logger.info(f"📡 Endpoint: POST /run_test")
    logger.info(f"🔑 Keyword: {req.keyword}")
    logger.info(f"📊 Test Data: {req.payload}")
    logger.info("-" * 60)
    
    result = run_test(req.keyword, req.payload)
    return {"status": "ok", "result": result}
