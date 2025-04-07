from fastapi import FastAPI
from pydantic import BaseModel
import requests
import datetime

app = FastAPI()

API_KEY = "321f2b36-0d57-4785-8f4b-8c660205aa75"
HELIUS_URL = f"https://mainnet.helius-rpc.com/?api-key={API_KEY}"

class Payload(BaseModel):
    data: dict

@app.post("/")
async def webhook_handler(payload: Payload):
    print("✅ Received webhook:", payload.data)
    return {"status": "success"}

@app.get("/check-new-tokens")
async def check_new_tokens():
    now = datetime.datetime.utcnow()
    start_ts = int((now - datetime.timedelta(seconds=60)).timestamp() * 1000)
    end_ts = int(now.timestamp() * 1000)

    body = {
        "jsonrpc": "2.0",
        "id": "new-tokens",
        "method": "getTransactions",
        "params": {
            "types": ["INITIALIZE_MINT", "CREATE_ACCOUNT"],
            "startSlot": start_ts,
            "endSlot": end_ts,
            "limit": 20
        }
    }

    try:
        res = requests.post(HELIUS_URL, json=body)
        txs = res.json().get("result", [])

        tokens = []
        for tx in txs:
            if isinstance(tx, dict):
                tokens.append(tx.get("signature", "no-signature"))
            else:
                print("⚠️ 非预期 tx 类型:", type(tx), tx)

        return {"new_tokens": tokens}
    except Exception as e:
        print("❌ 错误:", str(e))
        return {"error": "failed to query helius"}
