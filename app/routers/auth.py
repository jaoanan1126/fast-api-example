from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, schemas, models, utils, oath2

router = APIRouter(
    # prefix="auth",
    tags=["Authentication"]
)

#  To access token, login first then take the authorization. Copy that authorization and send that to the header of the API
@router.post("/login", response_model=schemas.Token)
# Note the oathPassword request form requests it in form data 
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not user: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
            detail=f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
            detail=f"Invalid Credentials")
    # Create a token
    # return token
    access_token = oath2.create_access_token(data = {"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}