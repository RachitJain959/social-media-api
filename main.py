from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello world"}

@app.get("/posts")
def get_posts():
    return {"data": "These are all your posts."}

@app.post("/createposts")
def create_posts(payLoad: dict = Body(...)):
    print(payLoad)
    return {"message": "successfully created the post!"}