from fastapi import FastAPI , HTTPException 
from pydantic import BaseModel

text_post = {"1":{"title":"new post" , "content":"this is my first post"} ,
             "2":{"title":"new post" , "content":"this is my second post" },
             "3":{"title":"new post" , "content":"this is my third post"}}
app = FastAPI()

class post(BaseModel):
    title:str
    content:str


@app.get("/posts")
def get_posts():
    if not text_post:
        raise HTTPException(status_code = 404 , details = "no post")
    return text_post
@app.get("/posts/{id}")
def get_post(id:str):
    if id not in text_post:
         raise HTTPException(status_code = 404 , detail = "post not found")
    post = text_post.get(id)
    return post

@app.post("/posts")

def create_post(post:post):
    new_post = {"title": post.title, "content": post.content}
    id = len(text_post) + 1
    text_post[id] = new_post
    return new_post

@app.get("/")
def read_root():
    return{"message" : "hello from Aryan"}
