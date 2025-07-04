# app/models/workout.py

from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.core.database import Base


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    # ✅ 1. Combina as duas versões: um nome é obrigatório (da main) e indexado (da sua branch).
    name = Column(String, index=True, nullable=False)
    description = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)

    # ✅ 2. Adota o modelo mais completo da sua branch, com IDs separados para treinador e aluno.
    trainer_id = Column(Integer, ForeignKey("users.id"))
    student_id = Column(Integer, ForeignKey("users.id"))

    # ✅ 3. Mantém os relacionamentos explícitos e bem definidos da sua branch.
    # Isso é crucial para o SQLAlchemy entender as múltiplas conexões com a tabela User.
    trainer = relationship(
        "User", foreign_keys=[trainer_id], back_populates="created_workouts"
    )
    student = relationship(
        "User", foreign_keys=[student_id], back_populates="assigned_workouts"
    )
