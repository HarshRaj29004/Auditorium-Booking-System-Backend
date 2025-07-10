from jwt import InvalidTokenError, ExpiredSignatureError, decode as jwt_decode
from fastapi import Request, HTTPException, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from utils.utils import SECRET_KEY

security = HTTPBearer()

def decode_access_token(token: str):
    try:
        payload = jwt_decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token decoding failed"
        )

def jwt_required(credential: HTTPAuthorizationCredentials = Depends(security)):
    if not credential:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized user"
        )

    token = credential.credentials
    payload = decode_access_token(token)

    return payload
