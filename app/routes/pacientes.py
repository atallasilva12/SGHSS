from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter(
    prefix="/pacientes",
    tags=["Pacientes"]
)

class Paciente(BaseModel):
    id: int
    nome: str
    email: str
    telefone: str
    data_nascimento: str
    historico_medico: Optional[str] = ""

pacientes_db = []

def fake_get_usuario_atual():
    return {"email": "teste@teste.com"}

@router.post("")
def criar_paciente(paciente: Paciente, usuario: dict = Depends(fake_get_usuario_atual)):
    pacientes_db.append(paciente)
    return paciente

@router.get("", response_model=List[Paciente])
def listar_pacientes(usuario: dict = Depends(fake_get_usuario_atual)):
    return pacientes_db
