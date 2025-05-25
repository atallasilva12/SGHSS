from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from jose.exceptions import JWTError  # ✅ Importação correta!
from pydantic import BaseModel

router = APIRouter()
SECRET_KEY = "minha-chave-secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# -------------------- Banco temporário --------------------
usuarios_db = {}

# -------------------- MODELOS --------------------
class Usuario(BaseModel):
    email: str
    senha: str
    tipo: str

# -------------------- FUNÇÕES DE AUTENTICAÇÃO --------------------
def autenticar_usuario(email: str, senha: str):
    user = usuarios_db.get(email)
    if not user or not pwd_context.verify(senha, user["senha_hash"]):
        return None
    return user

def criar_token_acesso(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_usuario_atual(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        user = usuarios_db.get(email)
        if user is None:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

# -------------------- ROTAS --------------------
@router.post("/signup")
def signup(usuario: Usuario):
    if usuario.email in usuarios_db:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    senha_hash = pwd_context.hash(usuario.senha)
    usuarios_db[usuario.email] = {
        "email": usuario.email,
        "senha_hash": senha_hash,
        "tipo": usuario.tipo
    }
    return {"mensagem": "Usuário criado com sucesso"}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = autenticar_usuario(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    access_token = criar_token_acesso(
        data={"sub": user["email"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}
