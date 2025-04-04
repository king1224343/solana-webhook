from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

@app.post("/")
async def webhook_listener(request: Request):
    data = await request.json()
    print("🔔 Webhook Triggered!")
    print(data)
    return {"status": "received", "data": data}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
