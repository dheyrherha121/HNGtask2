from pydantic import BaseModel,EmailStr,Field


class User(BaseModel):
   
    firstName:str=  Field(min_length=1 )
    lastName:str=Field(min_length=1)
    email: EmailStr
    password:str=Field(min_length=8)
    email:str=Field(min_length=10)   

class userResponse(BaseModel):
    userId: str
    firstName: str
    lastName: str
    email: EmailStr
    phone:str

class RegisterResponseData(BaseModel):
    accesToken: str
    user: userResponse    

class RegisterResponse(BaseModel):
    status: str
    message: str
    data: RegisterResponseData

class Organisation(BaseModel):
    name: str = Field(min_length=1)
    description:str        

class OrganisationResponse(BaseModel):
    orgId: str
    name: str
    description:str     