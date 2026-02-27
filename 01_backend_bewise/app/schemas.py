from datetime import datetime

from pydantic import BaseModel, Field


class QuestionBase(BaseModel):
    id: int = Field(..., description="ID записи в нашей БД")
    external_id: int = Field(..., description="ID вопроса во внешнем API")
    question: str
    answer: str
    created_at: datetime


class QuestionResponse(QuestionBase):
    class Config:
        from_attributes = True


class QuestionsRequest(BaseModel):
    questions_num: int = Field(..., gt=0, description="Количество новых вопросов")

