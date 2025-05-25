from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext

app = FastAPI(title="SGHSS API", version="1.0")

# -----------------------------
# CONFIGURAÇÃO DO JWT E SEGURANÇA
# -----------------------------
SECRET_KEY = "minha-chave-secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# -----------------------------
# MODELOS
# -----------------------------
class Usuario(BaseModel):
    email: str
    senha: str
    tipo: str  # 'paciente', 'profissional', 'admin'

class UsuarioDB(Usuario):
    senha_hash: str

class Paciente(BaseModel):
    id: int
    nome: str
    email: str
    telefone: str
    data_nascimento: str
    historico_medico: Optional[str] = ""

class Consulta(BaseModel):
    id: int
    paciente_id: int
    profissional_id: int
    data_hora: datetime
    observacoes: Optional[str] = ""

# -----------------------------
# DADOS EM MEMÓRIA (temporário)
# -----------------------------
usuarios_db = {}
pacientes = []
consultas = []

# -----------------------------
# FUNÇÕES DE SEGURANÇA
# -----------------------------
def autenticar_usuario(email: str, senha: str):
    user = usuarios_db.get(email)
    if not user:
        return None
    if not pwd_context.verify(senha, user["senha_hash"]):
        return None
    return user

def criar_token_acesso(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
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

# -----------------------------
# ROTAS DE AUTENTICAÇÃO
# -----------------------------
@app.post("/signup")
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

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = autenticar_usuario(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    access_token = criar_token_acesso(
        data={"sub": user["email"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

# -----------------------------
# ROTAS DE PACIENTES
# -----------------------------
@app.post("/pacientes")
def criar_paciente(usuario):
    print(usuario['email'])  # exemplo de uso

@app.get("/pacientes", response_model=List[Paciente])
def listar_pacientes(usuario: dict = Depends(get_usuario_atual)):
    return pacientes

# -----------------------------
# ROTAS DE CONSULTAS
# -----------------------------
@app.post("/consultas")
def marcar_consulta(consulta: Consulta, usuario: dict = Depends(get_usuario_atual)):
    consultas.append(consulta)
    return consulta

@app.get("/consultas/paciente/{paciente_id}", response_model=List[Consulta])
def listar_consultas(paciente_id: int, usuario: dict = Depends(get_usuario_atual)):
    return [c for c in consultas if c.paciente_id == paciente_id]

# -----------------------------
# INSTRUÇÃO DE EXECUÇÃO
# -----------------------------
# Execute com: uvicorn main:app --reload
