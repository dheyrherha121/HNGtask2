from .. import models,database,schema,utility
from fastapi import APIRouter,status,Depends,HTTPException


from sqlalchemy.orm import session

from uuid import uuid4
router = APIRouter(
    prefix= '/auth',
    tags= ['auth']
)
@router.post('/register',status_code=status.HTTP_201_CREATED, response_model=schema.RegisterResponse)
def create_user(request: schema.User, db: session=Depends(database.get_db)):
    user_id=str(uuid4())
    userInDb=db.query(models.User).filter(models.User.email== request.email).first()
    if userInDb:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, details='Email already registered' )
    
    #hash the password from user password
    hash_password = utility.hash(request.password)
    new_user= models.User(
        userId=user_id,
        firstName=request.firstName,
        lastName=request.lastName,
        email=request.email,
        password=hash_password,
        phone=request.phone
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    org_id= str(uuid4())
    org_name=f"{request.firstName}'s organisation"
    new_org=models.Organisation(orgId=org_id, name=org_name, description='')
    db.add(new_org)
    db.commit()
    db.refresh(new_org)

    user_org= models.UserOrganisation(user_id=new_user.userId, org_id=new_org.orgId)
    db.add(user_org)
    db.commit()

    access_token=utility.create_access_token(data={'sub':new_user.email})
    return schema.RegisterResponse(
        status='Success',
        message='Registration Successful',
        data=schema.RegisterResponseData(
            accesToken=access_token,
            user=schema.userResponse(
                userId=new_user.userId,
                firstName=new_user.firstName,
                lastName=new_user.lastName,
                email=new_user.email,
                phone=new_user.phone
            )
        ) 
    )
@router.post('/login', response_model=schema.RegisterResponse, status_code=status.HTTP_201_CREATED)
def login(request:schema.User, db: session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user or utility.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
    access_token=utility.create_access_token(data={'sub':user.email})
    return schema.RegisterResponse(
        status='Success',
        message='Login Successful',
        data=schema.RegisterResponseData(accesToken=access_token,
                                         user=schema.userResponse(
                                             userId=user.userId,
                                             firstName=user.firstName,
                                             lastName=user.lastName,
                                             email=user.email,
                                             phone=user.phone
                                         ))
    )

    