from datetime import datetime, date

from pydantic import BaseModel


class Concept(BaseModel):
    """
    id : concept id
    concept_name : concept 이름
    domain_id : concept가 주로 사용되는 도메인(카테고리)
    """

    id: int
    concept_name: str
    domain_id: str

    class Config:
        orm_mode = True


class Person(BaseModel):
    """
    id : int 환자 id
    gender_concept_id : int 성별 id
    birth_datetime : datetime 생년월일
    race_concept_id : int 인종 id
    ethnicity_concept_id : int 민족 id
    """

    id: int
    gender_concept_id: Concept
    birth_datetime: datetime
    race_concept_id: Concept
    ethnicity_concept_id: Concept

    class Config:
        orm_mode = True
