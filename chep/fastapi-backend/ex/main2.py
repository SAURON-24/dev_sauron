#(myenv) [root@master /work/dev_sauron/chep/fastapi-backend]# uvicorn main:app --reload --host 0.0.0.0 --port 8000
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 필요한 도메인만 추가하세요.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

