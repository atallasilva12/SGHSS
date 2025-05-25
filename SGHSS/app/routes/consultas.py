from fastapi import APIRouter, Depends
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class Consulta(BaseModel):
    id: int
    paciente_id: int
    profissional_id: int
    data_hora: datetime
    observacoes: Optional[str] = ""

consultas_db = []

def fake_get_usuario_atual():
    return {"email": "teste@teste.com"}  # Substitua depois com autenticação real

@router.post("/consultas")
def marcar_consulta(consulta: Consulta, usuario: dict = Depends(fake_get_usuario_atual)):
    consultas_db.append(consulta)
    return consulta

@router.get("/consultas/paciente/{paciente_id}", response_model=List[Consulta])
def listar_consultas(paciente_id: int, usuario: dict = Depends(fake_get_usuario_atual)):
    return [c for c in consultas_db if c.paciente_id == paciente_id]
