
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from datetime import datetime
from typing import Optional

# Clave secreta utilizada para firmar el token (debería ser segura en un entorno de producción)
SECRET_KEY = "clave_secreta"

# Algoritmo de firma (puedes usar HS256 u otro algoritmo compatible con PyJWT)
ALGORITHM = "HS256"

# Tiempo de expiración del token (por ejemplo, 30 minutos)
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(email: str):
    # Calcula la fecha y hora de expiración del token
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expires_at = datetime.utcnow() + expires_delta

    # Crea un payload (contenido) para el token con la información del usuario
    payload = {
        "sub": email,           # Sujeto del token (generalmente el identificador del usuario)
        "exp": expires_at       # Fecha y hora de expiración del token
    }

    # Genera el token JWT firmado
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token

# Función para verificar el token
def verify_token(token: str, required_claims: Optional[dict] = None):
    try:
        # Decodifica y verifica el token utilizando la clave secreta y el algoritmo
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Verifica si el token ha expirado
        exp_timestamp = payload.get("exp", None)
        if exp_timestamp is not None:
            exp_datetime = datetime.utcfromtimestamp(exp_timestamp)
            if exp_datetime < datetime.utcnow():
                raise HTTPException(status_code=401, detail="Token ha expirado")

        # Si se proporciona el argumento `required_claims`, verifica que se cumplan los reclamos requeridos
        if required_claims:
            for key, value in required_claims.items():
                if key not in payload or payload[key] != value:
                    raise HTTPException(status_code=401, detail="Token no válido")

        return payload  # Devuelve el contenido del token (payload)

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token ha expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token no válido")
