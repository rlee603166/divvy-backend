from typing import Optional
from httpx import stream
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    status: str
    message: str
    
class Token(BaseModel):
    status: str
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str
    
class RegisterToken(BaseModel):
    status: str
    register_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserBase(BaseModel):
    username: str
    phone: str | None = None

class UserCreate(BaseModel):
    name: str
    username: str
    phone: str
    imageUri: str | None = None

class UserUpdate(BaseModel):
    user_id: int | None = None
    name: str | None = None
    username: str | None = None
    imageUri: str | None = None
    phone: str | None = None
   
class AuthForm(BaseModel):
    username: Optional[str] = None
    phone: Optional[str] = None
    code: Optional[str] = None

class RegAuth(BaseModel):
    phone: str
    code: str

class Venmo(BaseModel):
    name: str
    photo_url: str
    username: str
    handle: str

class RegisterForm(BaseModel):
    name: str
    username: str
    phone: str
    imageUri: str | None = None

class NewUser(BaseModel):
    user_id: int
    username: str
    created_at: str
    phone: str


class User(BaseModel):
    user_id: int | None = None
    name: str | None = None
    username: str | None = None
    phone: str | None = None
    created_at: str | None = None
    imageUri: str | None = None

class UserInDB(BaseModel):
    user_id: int | None = None
    name: str | None = None
    username: str | None = None
    phone: str | None = None
    created_at: str | None = None
    imageUri: str | None = None
    friend_id: int | None = None
    status: str | None = None

class CreateFriendShip(BaseModel):
    user_1: int
    user_2: int
    status: str

class FriendShip(BaseModel):
    user_1: int
    user_2: int
 

class GetFriends(BaseModel):
    user_1: int
    friend_id: int
    status: str
