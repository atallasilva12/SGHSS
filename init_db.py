from app.database import engine
from app.models.paciente import Base  # ou ajuste conforme onde estiver o Base


print("Criando tabelas no banco de dados...")
Base.metadata.create_all(bind=engine)
print("Tabelas criadas com sucesso!")
