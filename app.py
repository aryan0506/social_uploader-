from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Annotated
import uuid
import shutil
import tempfile
import os

from database import Base, engine, get_db
from schema import Post , User
from images import imagekit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions

from users import fastapi_users, auth_backend, current_active_user
from models import UserCreate, UserRead, UserUpdate

app = FastAPI()


@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


db_dependency = Annotated[AsyncSession, Depends(get_db)]


@app.post("/upload")
async def upload_file(
    db: db_dependency,
    file: UploadFile = File(...),
    caption: str = Form(...),
    user: User = Depends(current_active_user)
):
    temp_file_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=os.path.splitext(file.filename)[1]
        ) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)

        upload_result = imagekit.upload_file(
            file=open(temp_file_path, "rb"),
            file_name=file.filename,
            options=UploadFileRequestOptions(
                use_unique_file_name=True, tags=["backend-upload"]
            ),
        )

        if upload_result.response_metadata.http_status_code == 200:
            post = Post(
                user_id = user.id,
                caption=caption,
                url=upload_result.url,
                file_type="video"
                if file.content_type.startswith("video/")
                else "image",
                file_name=upload_result.name,
            )

            db.add(post)
            await db.commit()
            await db.refresh(post)

            return post

    except Exception as e:
        raise HTTPException(500, str(e))

    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()


@app.get("/view")
async def view(db: db_dependency, user :User = Depends(current_active_user)):
    result = await db.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]

    result = await db.execute(select(User))
    users = [row[0] for row in result.all()]
    user_dict = {u.id:u.email  for u in users}

    return {
        "posts": [
            {
                "id": str(p.id),
                "user_id": str(p.user_id),
                "caption": p.caption,
                "url": p.url,
                "file_type": p.file_type,
                "file_name": p.file_name,
                "created_at": p.created_at.isoformat(),
                "is_owner":p.user_id == user.id,
                "email": user_dict.get(p.user_id , "Unknown")
            }
            for p in posts
        ]
    }


@app.delete("/posts/{post_id}")
async def delete_post(
    post_id: str, db: db_dependency, user: User = Depends(current_active_user)
):
    try:
        post_uuid = uuid.UUID(post_id)

        result = await db.execute(select(Post).where(Post.id == post_uuid))
        post = result.scalars().first()

        if not post:
            raise HTTPException(404, "Post not found")
        
        if post.user_id != user.id:
            raise HTTPException(403, "You don't have permission to delete this post")

        await db.delete(post)
        await db.commit()

        return {"success": True, "message": "Post deleted successfully"}

    except Exception as e:
        raise HTTPException(500, str(e))


# AUTH ROUTES
app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
