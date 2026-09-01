from fastapi import FastAPI, Request, Header, HTTPException
import hmac
import hashlib
import json
import os
from enum import Enum

app = FastAPI(title="ResQconnect / Aegis Treasury Marketplace Webhook")

WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "")

class MarketplaceEvent(str, Enum):
    PURCHASE = "marketplace_purchase"
    CHANGE = "marketplace_change"
    CANCELLED = "marketplace_cancelled"


def verify_github_signature(body: bytes, signature: str) -> bool:
    if not WEBHOOK_SECRET:
        return False
    sha_name, signature = signature.split("=", 1)
    mac = hmac.new(WEBHOOK_SECRET.encode(), msg=body, digestmod=hashlib.sha1)
    return hmac.compare_digest(mac.hexdigest(), signature)


@app.post("/webhook")
async def github_webhook(request: Request, x_hub_signature: str = Header(None), x_github_event: str = Header(None)):
    body = await request.body()
    if x_hub_signature is None:
        raise HTTPException(status_code=400, detail="Missing X-Hub-Signature header")
    if not verify_github_signature(body, x_hub_signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    payload = json.loads(body)
    event = x_github_event

    # Basic routing for marketplace events
    if event == MarketplaceEvent.PURCHASE:
        # TODO: validate payload structure and persist purchase
        # Example: payload['marketplace_purchase']['account']['id'] etc.
        # For now, just acknowledge and log
        print("Marketplace purchase received:", json.dumps(payload)[:500])
        # call provisioning logic (stub)
        # from licensing.service import provision_tenant
        # provision_tenant(payload)
        return {"status": "ok", "event": event}

    if event == MarketplaceEvent.CHANGE:
        print("Marketplace change received")
        return {"status": "ok", "event": event}

    if event == MarketplaceEvent.CANCELLED:
        print("Marketplace cancelled received")
        return {"status": "ok", "event": event}

    return {"status": "ignored", "event": event}
