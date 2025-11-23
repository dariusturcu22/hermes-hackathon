from fastapi import Security, APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
import requests
from sqlalchemy.orm import Session

from .schemas import SignupRequest
from .utils import VerifyToken
from ..config import get_settings
from ..database import get_db
from ..users.schema import UserCreate
from ..users.service import UserService

router = APIRouter(prefix="/auth", tags=["Authentication"])

auth = VerifyToken()


@router.get("/api/public")
def public():
    """No access token required to access this route"""

    result = {
        "status": "success",
        "msg": ("Hello from a public endpoint! You don't need to be "
                "authenticated to see this.")
    }
    return result


@router.get("/api/private")
def private(auth_result: str = Security(auth.verify)):
    """A valid access token is required to access this route"""
    return auth_result


@router.post("/signup")
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    """Register a new user in Auth0 AND create a local DB user"""

    url = f"https://{get_settings().auth0_domain}/dbconnections/signup"
    payload = {
        "client_id": get_settings().auth0_client_id,
        "email": data.email,
        "password": data.password,
        "connection": "Username-Password-Authentication"
    }

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    auth0_result = response.json()

    auth0_user_id = auth0_result.get("user_id") or auth0_result.get("_id")
    if not auth0_user_id:
        raise HTTPException(status_code=500, detail="Auth0 did not return a user ID")

    user_data = UserCreate(
        auth0_id=auth0_user_id,
        name=data.name if hasattr(data, "name") and data.name else data.email.split("@")[0],
        email=data.email,
        role="volunteer",
        total_points=0
    )

    try:
        local_user = UserService.create_user(db, user_data)
    except HTTPException as e:
        return {"success": False, "detail": str(e.detail), "auth0": auth0_result}

    return {
        "success": True,
        "auth0": auth0_result,
        "user": {
            "id": local_user.id,
            "auth0_id": local_user.auth0_id,
            "name": local_user.name,
            "email": local_user.email,
            "role": local_user.role,
            "total_points": local_user.total_points
        }
    }


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate user and get JWT from Auth0"""
    url = f"https://{get_settings().auth0_domain}/oauth/token"
    payload = {
        "grant_type": "http://auth0.com/oauth/grant-type/password-realm",
        "username": form_data.username,
        "password": form_data.password,
        "audience": get_settings().auth0_api_audience,
        "client_id": get_settings().auth0_client_id,
        "client_secret": get_settings().auth0_client_secret,
        "realm": "Username-Password-Authentication",
        "scope": "openid profile email"
    }

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()
