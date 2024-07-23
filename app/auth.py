from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
import db, models, auth, schemas, crud
from passlib.context import CryptContext
router = APIRouter()

# Ruta para servir el formulario de inicio de sesión
@router.get("/login", response_class=HTMLResponse)
async def login_form():
    return """
    <html>
        <head>
            <title>Login</title>
            <script>
                async function handleLogin(event) {
                    event.preventDefault();
                    const form = event.target;
                    const formData = new FormData(form);
                    const data = {
                        username: formData.get('username'),
                        password: formData.get('password')
                    };
                    const response = await fetch('/login', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded'
                        },
                        body: new URLSearchParams(data)
                    });
                    const result = await response.json();
                    if (response.ok) {
                        localStorage.setItem('token', result.access_token);
                        alert('Login successful!');
                    } else {
                        alert('Login failed: ' + result.detail);
                    }
                }
            </script>
        </head>
        <body>
            <form onsubmit="handleLogin(event)">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password">
                <button type="submit">Login</button>
            </form>
        </body>
        <script>
    async function fetchProtectedData() {
        const token = localStorage.getItem('token');
        const response = await fetch('/users/me/', {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + token
            }
        });
        const data = await response.json();
        if (response.ok) {
            console.log('Protected data:', data);
        } else {
            console.error('Failed to fetch protected data:', data);
        }
    }

    document.addEventListener('DOMContentLoaded', fetchProtectedData);
</script>

    </html>
    """


# Ruta para procesar el formulario de inicio de sesión
@router.post("/login")
async def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(db.get_db)):
    user = auth.authenticate_user(db, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}





# Configuración del token JWT
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Contexto de la contraseña
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 esquema de contraseña
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Crear y verificar hashes de contraseñas
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# Obtener usuario por username
def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

# Autenticar usuario
def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Crear un token de acceso
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Obtener el usuario actual a partir del token
async def get_current_user(db: Session = Depends(db.get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=username)
    if user is None:
        raise credentials_exception
    return user

# Verificar si el usuario actual es un admin
async def get_current_admin_user(current_user: schemas.User = Depends(get_current_user)):
    if current_user.role != schemas.RoleEnum.admin:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    return current_user

#crear un usuario
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        hashed_password=hashed_password,
        email=user.email,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user