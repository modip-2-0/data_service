from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import JSONResponse
from jose import jwt
import bcrypt
from datetime import datetime, timedelta, timezone

from models.user import UserIn
from crud.user import create_user, get_user_by_email, get_user_db_by_email
from api.dependencies import AsyncMongoDB

router = APIRouter()

SECRET = "1652e68e6e5c4c9d21c6c38a87c143ea3f0b865fe318fae0374de808f5f0016f"
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 10  # minutos

@router.post("/register")
async def register(db: AsyncMongoDB, user: UserIn):
    # Verificar si el email ya existe
    try:
        await get_user_by_email(db, user.email)
        return JSONResponse(
            status_code=409,
            content={"message": f"User with email {user.email} already exists."}
        )
    except HTTPException as e:
        if e.status_code != 404:
            raise e

    try:
        # Hashear contraseña
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(user.password.encode('utf-8'), salt)
        # Crear usuario en BD
        new_user = await create_user(db, user.email, user.name, hashed.decode('utf-8'))
        # Generar token con _id como sub
        token_data = {
            "sub": str(new_user.id),      # ← ObjectId a string
            "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION),
            "email": user.email           # claim adicional (opcional)
        }
        token = jwt.encode(token_data, SECRET, algorithm=ALGORITHM)
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Internal error: {str(e)}"})

@router.post("/login")
async def login(db: AsyncMongoDB, credentials: list = Body(...)):
    # credentials = [email, password]
    email = credentials[0]
    password = credentials[1]

    try:
        user_db = await get_user_db_by_email(db, email)
    except HTTPException:
        return JSONResponse(status_code=401, content={"message": "User does not exist. Please register."})

    # Verificar contraseña
    if not bcrypt.checkpw(password.encode('utf-8'), user_db.hashed_password.encode('utf-8')):
        return JSONResponse(status_code=401, content={"message": "Invalid password."})

    # Generar token con _id como sub
    token_data = {
        "sub": str(user_db.id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION),
        "email": user_db.email
    }
    token = jwt.encode(token_data, SECRET, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}



# (Opcional) Endpoint protegido que devuelve el usuario actual
# Si quieres usarlo, necesitas crear la dependencia get_current_user (más abajo)




# from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
# from fastapi.responses import JSONResponse
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jose import jwt
# import bcrypt
# from datetime import datetime, timedelta, timezone

# from models.user import UserIn, UserDB, UserOut
# from crud.user import create_user, get_user, get_userDB
# from api.dependencies import AsyncMongoDB


# ALGORITHM = "HS256"
# SECRET = "1652e68e6e5c4c9d21c6c38a87c143ea3f0b865fe318fae0374de808f5f0016f"
# ACCESS_TOKEN_DURATION = 60


# router = APIRouter()


# oauth2 = OAuth2PasswordBearer(tokenUrl="login")


# @router.post("/register")
# async def auth(db: AsyncMongoDB, user: UserIn):

#     try:
#         user: UserOut = await get_user(db, user.username)  
#         return JSONResponse(
#             status_code=500,
#             content={"message": f"User {user.username} already exists."}
#         )
#     except HTTPException:
#         pass

#     try:        
 

#         salt = bcrypt.gensalt()
#         hashed_password = bcrypt.hashpw(user.password.encode(), salt)

#         user.password = hashed_password.decode('utf-8')  # Store as string

#         await create_user(db, user)     

#         access_token = {
#             "sub": user.username,
#             "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION),            
#         }     
     
#         return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type":"bearer"}  
    
#     except HTTPException:
#         raise  # Re-lanza las excepciones HTTP ya manejadas
#     except Exception as e:
#         return JSONResponse(
#             status_code=500,
#             content={"message": f"Error interno del servidor: {str(e)}"}
#         )


# @router.post("/login")
# async def login(db: AsyncMongoDB, credentials: list = Body(...)):

#     username = credentials[0]
#     password = credentials[1]

#     try:
        
#         user: UserDB = await get_userDB(db, username)            
        
#         hashed_password = user.password.encode('utf-8')
#         if not bcrypt.checkpw(password.encode(), hashed_password): 
#             return JSONResponse(
#             status_code=500,
#             content={"message": "Password do not match."}
#         )        
 
        
#         access_token = {
#             "sub": username,
#             "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION),            
#         }     
     
#         return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type":"bearer"}  

#     except HTTPException:
#         return JSONResponse(
#             status_code=500,
#             content={"message": f"User {username} does not exist, please register."}
#         )   
#     except Exception as e:        
#         return JSONResponse(
#             status_code=500,
#             content={"message": f"Error interno del servidor: {str(e)}"}
#         )


# @router.get("/user/{username}", response_model=UserOut)
# async def get(db: AsyncMongoDB, username: str) -> UserOut:
#     return await get_user(db, username)      
