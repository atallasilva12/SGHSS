from fastapi import FastAPI
from app.routes import pacientes, consultas, auth

app = FastAPI(title="SGHSS API", version="1.0")

# Inclui as rotas
app.include_router(auth.router)
app.include_router(pacientes.router)
app.include_router(consultas.router)
