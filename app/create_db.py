from app.core.database import Base, engine
from app.models.user import User

print("Criando tabelas...")
Base.metadata.create_all(bind=engine)
print("OK.")
