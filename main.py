from fastapi import FastAPI
from utils import get_recent_mint_transactions

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Solana Token Scanner is running."}

@app.get("/check-new-tokens")
async def check_new_tokens():
    tokens = await get_recent_mint_transactions()
    return {"tokens": tokens}
