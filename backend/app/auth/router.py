from fastapi import Security, APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
import requests

from .schemas import SignupRequest
from .utils import VerifyToken
from ..config import get_settings

router = APIRouter(prefix="/auth", tags=["Authentication"])

auth = VerifyToken()  # 👈 Get a new instance


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
def private(auth_result: str = Security(auth.verify)):  # Use Security and the verify method to protect your endpoints
    """A valid access token is required to access this route"""
    return auth_result


@router.post("/signup")
def signup(data: SignupRequest):
    """Register a new user in Auth0"""
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

    return response.json()


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate user and get JWT from Auth0"""
    url = f"https://{get_settings().auth0_domain}/oauth/token"
    payload = {
        "grant_type": "password",
        "username": form_data.username,
        "password": form_data.password,
        "audience": get_settings().auth0_api_audience,
        "client_id": get_settings().auth0_client_id,
        "client_secret": get_settings().auth0_client_secret
    }

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()
