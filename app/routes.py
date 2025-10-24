import logging
from fastapi import APIRouter, Header, HTTPException, status
from app.models import RoleChangeRequest, RoleRequest, RoleResponse, user
from app.utils import is_authorized, is_valid_role
from app.database import database

log = logging.getLogger(__name__)

router = APIRouter()
    
@router.get("/role", response_model=RoleResponse)
async def get_user_role(
    request: RoleRequest,
    x_forwarded_email: str = Header(None)):

    # Check if the requestor email exists and is allowed to make changes
    if not x_forwarded_email or not is_authorized(x_forwarded_email):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized access")

    try:
        query = user.select().where(user.c.email == request.email)
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
    x_forwarded_email: str = Header(None),
):
    # Check if the requestor email exists and is allowed to make changes
    if not x_forwarded_email or not is_authorized(x_forwarded_email):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized access")

    # Validate the supplied role
    if not is_valid_role(request.role):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role")

    try:
        query = user.update().where(user.c.email == request.email).values(role=request.role)
        await database.execute(query)
        
        query = user.select().where(user.c.email == request.email)
        user_record = await database.fetch_one(query)

        if not user_record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        if request.role == user_record.role:
            return {"email": user_record.email, "role": user_record.role}
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update role")
        
    except Exception as e:
        log.error(f"Error updating user role: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    

@router.get("/health")
async def healthcheck():
    return {"status": True}

@router.get("/health/db")
async def healthcheck_with_db():
    try:
        query = user.select().limit(1)
        await database.fetch_one(query)        
        return {"status": True}
    except Exception as e:
        log.error(f"Database health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed",
        )
