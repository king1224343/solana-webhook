import os
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# 用于接收 webhook payload
class Payload(BaseModel):
    data: dict

@app.post("/")
async def webhook_handler(payload: Payload):
    print("🟢 Received webhook:", payload.data)
    return {"status": "success"}

# 测试用接口，Render 可用性验证
@app.get("/check-new-tokens")
async def check_tokens():
    return {"message": "接口已部署成功 🎉"}

# Render 自动注入 PORT 环境变量，适配主函数
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
