
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import  get_db
from sqlalchemy import func

from .. import models, schemas, utils, oath2


router = APIRouter(
    prefix= "/posts",
    tags=["Posts"]
)

# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user:int = Depends(oath2.get_current_user), 
              limit: int = 10, skip: int = 0, search: Optional[str] = "" ):
    # curs.execute("""SELECT * FROM post""")
    # posts = curs.fetchall()
    # print(posts)
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    # Limit is a parameter , define them in postman by doing posts?limit=1 / to do two you do posts?limit=1&skip=2
    # To search param with a space do: %20 ex: posts?limit=10&skip=1&search=Hello%20post
    # print(limit)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit=limit).offset(skip).all()
    # default left inner join 
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit=limit).offset(skip).all()
    # print("results ", results)
    return results

# Get requests - 
# Post - send data to API Server 
@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schemas.Post)
# Body takes all the params of the dictionary payload and turns it into the payload params 
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user:int = Depends(oath2.get_current_user)):
    # post_dict = post.dict()
    # post_dict['id']  = randrange(1,921242)
    # my_posts.append(post_dict)
    # curs.execute("""INSERT INTO post (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
    #              (posts.title, posts.content, posts.published)
    # )
    # new_post = curs.fetchone()
    # conn.commit()
    # new_post = models.Post(title=post.title, content = post.content, published = post.published )
    # These models are sql alchemy
    new_post = models.Post(owner_id = current_user.id, **post.dict()) # ** unpacks teh entire dict
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # related to return
    return new_post


# Naming conventions of URL 
    """
    Best practices
    Create: POST use plural nouns ex: /posts
    Read:
        GET /posts/{id} - one specific post
        GET /posts
    update
        PUT/PATCH /posts/{id}
        PUT - pass all info for updating 
        Patch - put specific field you want to change 
        
    Delete 
        DELETE  /posts/{id}
    """


# Title str, content str, category

@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user:int = Depends(oath2.get_current_user) ):
    # curs.execute("""SELECT * FROM post where id = %s""", 
    #             (str(id)))
    # post = curs.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post =  db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} was not found"
                            )
    return post

# def find_index_post(id):
#     for i,p in enumerate(my_posts):
#         if p['id'] == id:
#             return i

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id:int, db: Session = Depends(get_db), current_user:int = Depends(oath2.get_current_user)):
    # curs.execute("""DELETE FROM post where id = %s RETURNING *""",
    #              (str(id)))
    # del_post = curs.fetchone()
    # conn.commit()
    # if del_post == None: 
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"post with id: {id} does not exist" 
    #                         )
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    post_query = db.query(models.Post).filter(models.Post.id== id)
    post = post_query.first()
    
    if post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist" 
                            )
    if post.owner_id  != current_user.id: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to preform requested action" 
                            )
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",  response_model=schemas.Post)
def update_posts(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),current_user:int = Depends(oath2.get_current_user)):
    # curs.execute("""UPDATE post set title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
    #              (post.title, post.content, post.published, str(id)))
    # updated_post = curs.fetchone()
    # conn.commit()
    # if updated_post == None: 
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"post with id: {id} does not exist" 
    #                         )

    # return {"data": updated_post}
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist" 
                            )
    if post.owner_id != current_user.id: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to preform requested action" 
                            )
    post_query.update(updated_post.dict(), 
                      synchronize_session= False)
    db.commit()
    return post_query.first()
