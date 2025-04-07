import httpx
from datetime import datetime, timedelta, timezone

API_KEY = "321f2b36-0d57-4785-8f4b-8c660205aa75"
BASE_URL = "https://api.helius.xyz/v0/addresses"
DUMMY_ADDRESS = "11111111111111111111111111111111"

async def get_recent_mint_transactions():
    now = datetime.now(timezone.utc)
    one_minute_ago = now - timedelta(minutes=1)

    url = f"{BASE_URL}/{DUMMY_ADDRESS}/transactions?api-key={API_KEY}"

    headers = {"accept": "application/json"}
    body = {
        "limit": 100,
        "type": "INITIALIZE_MINT"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=body)

    txs = response.json()
    result = []

    for tx in txs:
        timestamp = datetime.fromisoformat(tx.get("timestamp", now.isoformat()))
        if timestamp >= one_minute_ago:
            result.append({
                "mint": tx.get("description", {}).get("mint"),
                "tx": tx.get("signature"),
                "time": timestamp.isoformat()
            })

    return result
