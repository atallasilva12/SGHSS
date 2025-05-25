from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import consultas, auth, pacientes
from fastapi.security import OAuth2PasswordBearer

# CORRETO agora para aparecer o botão "Authorize" no Swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI(title="SGHSS API", version="1.0")

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou ["http://localhost:8000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas
app.include_router(auth.router)
app.include_router(consultas.router)
app.include_router(pacientes.router)
