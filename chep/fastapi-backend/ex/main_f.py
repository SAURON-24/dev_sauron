from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Initial balance for user card
user_balance = 100000

# Product prices (for simplicity, we use fixed prices)
product_prices = {
    "product_1": 5000,
    "product_2": 10000,
}

# Sample UID mappings (these should be unique UIDs of your NFC tags)
uids = {
    "user_card": "0x5B 0x39 0x36 0x9",       # Example UID for user card
    "admin_card": "0xF4 0xA5 0xBD 0x49",      # Example UID for admin card
    "product_1": "0xCB 0x78 0xD0 0x15",       # Example UID for product 1
    "product_2": "0x9 0xB6 0xFB 0x62",       # Example UID for product 2
}

class NFCTag(BaseModel):
    tagId: str

@app.post("/nfc")
def read_nfc(tag: NFCTag):
    global user_balance
    
    tag_id = tag.tagId.upper()
    
    if tag_id == uids["admin_card"]:
        return {"message": "Admin card detected!!!!!!!!1", "balance": user_balance}
    
    if tag_id == uids["user_card"]:
        return {"message": f"User card detected~~~~~~~~~~ with balance: {user_balance}"}
    
    for product, uid in uids.items():
        if product != "user_card" and product != "admin_card" and tag_id == uid:
            if user_balance >= product_prices[product]:
                user_balance -= product_prices[product]
                return {"message": f"Product {product} purchased for {product_prices[product]} units", "balance": user_balance}
            else:
                return {"message": "Insufficient balance", "balance": user_balance}
    
    raise HTTPException(status_code=404, detail="Unknown tag")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
