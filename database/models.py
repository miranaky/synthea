from enum import Enum
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.schema import ForeignKeyConstraint

from .database import Base


class Person(Base):
    """
    환자에 대한 정보
    person_id : 환자 id
    gender_concept_id : 성별 id
    birth_datetime : 생년월일
    race_concept_id : 인종 id
    ethnicity_concept_id : 민족 id
    """

    __tablename__ = "person"
    __table_args__ = {"schema": "de"}

    id = Column("person_id", Integer, primary_key=True, index=True)
    gender_concept_id = Column("gender_concept_id", Integer, ForeignKey("de.concept.concept_id"))
    birth_datetime = Column("birth_datetime", DateTime)
    race_concept_id = Column("race_concept_id", Integer, ForeignKey("de.concept.concept_id"))
    ethnicity_concept_id = Column("ethnicity_concept_id", Integer, ForeignKey("de.concept.concept_id"))
    gender_concept = relationship("Concept", foreign_keys=[gender_concept_id], back_populates="gender_concept_person")
    race_concept = relationship("Concept", foreign_keys=[race_concept_id], back_populates="race_concept_person")
    ethnicity_concept = relationship(
        "Concept", foreign_keys=[ethnicity_concept_id], back_populates="ethnicity_concept_person"
    )


class VisitOccurrence(Base):
    """
    병원 방문에 대한 정보
    visit_occurrence_id : 방문 id
    person_id : 환자 id
    visit_concept_id : 방문 유형
        9201 : Inpatient Visit (입원)
        9202 : Outpatient Visit (외래)
        9203 : Emergency Room Visit (응급)
    visit_start_datetime : 방문 시작 일시
    visit_end_datetime : 방문 종료 일시
    """

    __tablename__ = "visit_occurrence"
    __table_args__ = {"schema": "de"}

    id = Column("visit_occurrence_id", Integer, primary_key=True, index=True)
    person_id = Column("person_id", Integer, ForeignKey("de.person.person_id"))
    visit_concept_id = Column("visit_concept_id", ForeignKey("de.concept.concept_id"))
    visit_start_datetime = Column("visit_start_datetime", DateTime)
    visit_end_datetime = Column("visit_end_datetime", DateTime)
    person = relationship("Person", backref=backref("visit", order_by=id))
    # concept = relationship("Concept", backref=backref("visit", order_by=id))


class ConditionOccurence(Base):
    """
    진단(병명)에 대한 정보
    person_id : 환자 id
    condition_concept_id : 진단(병명)
    condition_start_datetime : 진단 시작 일시
    condition_end_datetime : 진단 종료 일시
    visit_occurrence_id : 방문 id
    """

    __tablename__ = "condition_occurrence"
    __table_args__ = {"schema": "de"}

    id = Column("condition_occurrence_id", Integer, primary_key=True)
    person_id = Column("person_id", Integer, ForeignKey("de.person.id"))
    condition_concept_id = Column("condition_concept_id", Integer, ForeignKey("de.concept.id"))
    condition_start_datetime = Column("condition_start_datetime", DateTime)
    condition_end_datetime = Column("condition_end_datetime", DateTime)
    visit_occurrence_id = Column("visit_occurrence_id", Integer, ForeignKey("de.visit_occurrence.id"))


class DrugExposure(Base):
    """
    의약품 처방에 대한 정보
    person_id : 환자 id
    drug_concept_id : 처방 의약품
    drug_exposure_start_datetime : 처방 시작 일시
    drug_exposure_end_datetime : 처방 종료 일시
    visit_occurrence_id : 방문 id
    """

    __tablename__ = "drug_exposure"
    __table_args__ = {"schema": "de"}

    id = Column("drug_exposure_id", Integer, primary_key=True)
    person_id = Column("person_id", Integer, ForeignKey("de.person.id"))
    drug_concept_id = Column("drug_concept_id", Integer, ForeignKey("de.concept.id"))
    drug_exposure_start_datetime = Column("drug_exposure_start_datetime", DateTime)
    drug_exposure_end_datetime = Column("drug_exposure_end_datetime", DateTime)
    visit_occurrence_id = Column("visit_occurrence_id", Integer, ForeignKey("de.visit_occurrence.id"))


class Concept(Base):
    """
    여러 테이블에서 사용되는 concept들의 정보
    concept_id : concept id
    concept_name : concept 이름
    domain_id : concept가 주로 사용되는 도메인(카테고리)
    """

    __tablename__ = "concept"
    __table_args__ = {"schema": "de"}

    id = Column("concept_id", Integer, primary_key=True)
    concept_name = Column("concept_name", String(length=255))
    domain_id = Column("domain_id", String(length=20))
    gender_concept_person = relationship(
        "Person", foreign_keys=[Person.gender_concept_id], back_populates="gender_concept"
    )
    race_concept_person = relationship("Person", foreign_keys=[Person.race_concept_id], back_populates="race_concept")
    ethnicity_concept_person = relationship(
        "Person", foreign_keys=[Person.ethnicity_concept_id], back_populates="ethnicity_concept"
    )


class Death(Base):
    """
    환자의 사망 정보
    person_id : 환자 id
    death_date : 사망일
    """

    __tablename__ = "death"
    __table_args__ = {"schema": "de"}

    person_id = Column("person_id", Integer, ForeignKey("de.person.person_id"), primary_key=True)
    death_date = Column("death_date", DateTime)


class DomainName(str, Enum):
    Obs_or_Procedure = "Obs/Procedure"
    Metadata = "Metadata"
    Sponsor = "Sponsor"
    PlanStopReason = "Plan Stop Reason"
    Plan = "Plan"
    Ethnicity = "Ethnicity"
    SpecAnatomicSite = "Spec Anatomic Site"
    Geography = "Geography"
    Race = "Race"
    Episode = "Episode"
    Route = "Route"
    Unit = "Unit"
    Procedure = "Procedure"
    Device = "Device"
    Condition_or_Meas = "Condition/Meas"
    SpecDiseaseStatus = "Spec Disease Status"
    Condition_or_Procedure = "Condition/Procedure"
    Provider = "Provider"
    Drug = "Drug"
    TypeConcept = "Type Concept"
    Relationship = "Relationship"
    Observation = "Observation"
    Gender = "Gender"
    PlaceofService = "Place of Service"
    Measurement = "Measurement"
    Condition_or_Device = "Condition/Device"
    Currency = "Currency"
    Device_or_Procedure = "Device/Procedure"
    Payer = "Payer"
    MeasValue = "Meas Value"
    RevenueCode = "Revenue Code"
    Drug_or_Procedure = "Drug/Procedure"
    MeasValueOperator = "Meas Value Operator"
    Regimen = "Regimen"
    Cost = "Cost"
    Condition_or_Obs = "Condition/Obs"
    Visit = "Visit"
    Specimen = "Specimen"
    Condition = "Condition"
