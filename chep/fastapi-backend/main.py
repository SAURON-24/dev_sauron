from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# Initial balance for user card
user_balance = 10000000

# Product prices (for simplicity, we use fixed prices)
product_prices = {
    "국간장": {"price": 2000, "quantity": 0},
    "진간장": {"price": 1000, "quantity": 0},
    "설탕": {"price": 3000, "quantity": 0},
    "우유": {"price": 800, "quantity": 0}
}

# Sample UID mappings (these should be unique UIDs of your NFC tags)
uids = {
    "user_card": "D99EFA29",       # Example UID for user card
    "admin_card": "708D1A1A",      # Example UID for admin card
    "국간장": "5B393609",            # Example UID for product 1
    "진간장": "CB78D015",            # Example UID for product 2
    "설탕": "F4A5BD49",              # Example UID for product 3
    "우유": "09B6FB62"               # Example UID for product 4
}

admin_info = {
    "관리자명": "임영웅",
    "연락처": "010-1234-5678",
    "서비스구분": "무인편의점",
    "지점명": "히어로 편의점 강남지점",
    "주소": "서울특별시 강남구 테헤란로",
    "uid": uids["admin_card"]
}

user_info = {
    "유저명": "홍길동",
    "잔액": user_balance,
    "uid": uids["user_card"]
}

# Store detected objects
detected_objects: List[Dict[str, Any]] = []

class NFCTag(BaseModel):
    tagId: str

@app.post("/nfc")
async def read_nfc(tag: NFCTag):
    global user_balance
    tag_id = tag.tagId.upper()
    if tag_id == uids["admin_card"]:
        message = "Admin card detected"
        info = admin_info
    elif tag_id == uids["user_card"]:
        message = f"User card detected with balance: {user_balance}"
        info = user_info
    else:
        for product, data in product_prices.items():
            if product != "user_card" and product != "admin_card" and tag_id == uids[product]:
                if user_balance >= data["price"]:
                    user_balance -= data["price"]
                    data["quantity"] += 1
                    user_info["잔액"] = user_balance
                    message = {
                        "name": product,
                        "quantity": data["quantity"],
                        "price": data["price"]
                    }
                    info = {"balance": user_balance}
                    break
                else:
                    message = "Insufficient balance"
                    info = {"balance": user_balance}
                    break
        else:
            raise HTTPException(status_code=404, detail="Unknown tag")
    detected_objects.append({"message": message, "info": info})
    await manager.broadcast(message)
    return {"message": message, "info": info}

@app.get("/detected-objects")
def get_detected_objects():
    return detected_objects

@app.post("/clear-detected-objects")
def clear_detected_objects():
    global detected_objects
    detected_objects = []
    return {"message": "Detected objects cleared"}

@app.post("/start-payment")
async def start_payment():
    message = "Start payment process"
    await manager.broadcast(message)
    return {"message": message}

@app.post("/confirm-payment")
async def confirm_payment():
    message = "Payment confirmed"
    await manager.broadcast(message)
    return {"message": message}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
