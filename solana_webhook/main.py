from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Payload(BaseModel):
    data: dict

@app.post("/")
async def webhook_handler(payload: Payload):
    print("✅ Received webhook:", payload.data)
    return {"status": "success"}