# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel

# app = FastAPI()

# # Initial balance for user card
# user_balance = 100000

# # Product prices (for simplicity, we use fixed prices)
# product_prices = {
#     "국간장": 2000,
#     "진간장": 1000,
#     "설탕": 3000,
#     "우유": 800
# }

# # Sample UID mappings (these should be unique UIDs of your NFC tags)
# uids = {
#     "user_card": "D99EFA29",       # Example UID for user card
#     "admin_card": "708D1A1A",      # Example UID for admin card
#     "국간장": "5B393609",            # Example UID for product 1
#     "진간장": "CB78D015",            # Example UID for product 2
#     "설탕": "F4A5BD49",              # Example UID for product 3
#     "우유": "09B6FB62"               # Example UID for product 4
# }

# admin_info = {
#     "관리자명": "임영웅",
#     "연락처": "010-1234-5678",
#     "서비스구분": "무인편의점",
#     "지점명": "히어로 편의점 강남지점",
#     "주소": "서울특별시 강남구 테헤란로",
#     "uid": uids["admin_card"]
# }

# user_info = {
#     "유저명": "알렉세이",
#     "잔액": user_balance,
#     "uid": uids["user_card"]
# }

# # Store detected objects
# detected_objects = []

# class NFCTag(BaseModel):
#     tagId: str

# @app.post("/nfc")
# def read_nfc(tag: NFCTag):
#     global user_balance
    
#     tag_id = tag.tagId.upper()
    
#     if tag_id == uids["admin_card"]:
#         message = "Admin card detected"
#         info = admin_info
#     elif tag_id == uids["user_card"]:
#         message = f"User card detected with balance: {user_balance}"
#         info = user_info
#     else:
#         for product, uid in uids.items():
#             if product != "user_card" and product != "admin_card" and tag_id == uid:
#                 if user_balance >= product_prices[product]:
#                     user_balance -= product_prices[product]
#                     user_info["잔액"] = user_balance
#                     message = f"{product} purchased for {product_prices[product]} units"
#                     info = {"balance": user_balance}
#                     break
#                 else:
#                     message = "Insufficient balance"
#                     info = {"balance": user_balance}
#                     break
#         else:
#             raise HTTPException(status_code=404, detail="Unknown tag")
    
#     detected_objects.append({"message": message, "info": info})
#     return {"message": message, "info": info}

# @app.get("/detected-objects")
# def get_detected_objects():
#     return detected_objects

# @app.post("/clear-detected-objects")
# def clear_detected_objects():
#     global detected_objects
#     detected_objects = []
#     return {"message": "Detected objects cleared"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Initial balance for user card
user_balance = 100000

# Product prices (for simplicity, we use fixed prices)
product_prices = {
    "국간장": 2000,
    "진간장": 1000,
    "설탕": 3000,
    "우유": 800
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
    "유저명": "알렉세이",
    "잔액": user_balance,
    "uid": uids["user_card"]
}

# Store detected objects
detected_objects = []

class NFCTag(BaseModel):
    tagId: str

@app.post("/nfc")
def read_nfc(tag: NFCTag):
    global user_balance
    
    tag_id = tag.tagId.upper()
    print(f"Received tag ID: {tag_id}")
    
    if tag_id == uids["admin_card"]:
        message = "Admin card detected"
        info = admin_info
    elif tag_id == uids["user_card"]:
        message = f"User card detected with balance: {user_balance}"
        info = user_info
    else:
        for product, uid in uids.items():
            if product != "user_card" and product != "admin_card" and tag_id == uid:
                if user_balance >= product_prices[product]:
                    user_balance -= product_prices[product]
                    user_info["잔액"] = user_balance
                    message = f"{product} purchased for {product_prices[product]} units"
                    info = {"balance": user_balance}
                    break
                else:
                    message = "Insufficient balance"
                    info = {"balance": user_balance}
                    break
        else:
            raise HTTPException(status_code=404, detail="Unknown tag")
    
    detected_objects.append({"message": message, "info": info})
    return {"message": message, "info": info}

@app.get("/detected-objects")
def get_detected_objects():
    return detected_objects

@app.post("/clear-detected-objects")
def clear_detected_objects():
    global detected_objects
    detected_objects = []
    return {"message": "Detected objects cleared"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
