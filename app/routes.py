import logging
from pydantic import EmailStr
from fastapi import APIRouter, Header, HTTPException, status
from app.config import EMAIL_HEADER_NAME
from app.models import RoleResponse, RoleChangeRequest, user
from app.utils import is_valid_role
from app.database import database

log = logging.getLogger(__name__)

router = APIRouter()
    
@router.get("/role", response_model=RoleResponse)
async def get_user_role(forwarded_email: EmailStr = Header(None, alias=EMAIL_HEADER_NAME)):

    # Check if the requestor email exists and is allowed to make changes
    if not forwarded_email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized access")

    try:
        query = user.select().where(user.c.email == forwarded_email )
        user_record = await database.fetch_one(query)

        if user_record:
            return {"email": user_record.email, "role": user_record.role}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    except Exception as e:
        log.error(f"Error fetching user role: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
@router.post("/role", response_model=RoleResponse)
async def change_role(
    request: RoleChangeRequest,
    forwarded_email: str = Header(None, alias=EMAIL_HEADER_NAME),
):
    # Check if the requestor email exists and is allowed to make changes
    if not forwarded_email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized access")
    
    # Validate the supplied role
    if not is_valid_role(request.role):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role")
    
    try:
        # Update the user's role in the database
        query = user.update().where(user.c.email == forwarded_email).values(role=request.role)
        await database.execute(query)
        
        # Query the user details after update
        query = user.select().where(user.c.email == forwarded_email)
        user_record = await database.fetch_one(query)
        
        if not user_record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        return {"email": user_record.email, "role": user_record.role}
    except Exception as e:
        log.error(f"Error updating user role: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")