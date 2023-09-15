from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models, config
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

#path is from the auth file
oath2_scheme =  OAuth2PasswordBearer(tokenUrl='login')

#Secret key 
# Algorithm HS256
# Expiration time of the token

SECRET_KEY = config.settings.secret_key
ALGORITHM = config.settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = config.settings.access_token_minutes

def create_access_token(data: dict): 
    to_encode = data.copy()
    # Note it has to be UTC
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
            "exp": expire
    })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try: 
        # Note it's expected to be a list of algorithms 
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        id: str = payload.get("user_id")
        id = str(id)
        print("ID: ", id, type(id))
        if id is None: 
            raise credentials_exception
        token_data = schemas.TokenData(id = id)
    except JWTError:
        raise credentials_exception
    print(token_data)
    return token_data
    
def get_current_user(token:str = Depends(oath2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate credentials", 
                                headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception=credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user