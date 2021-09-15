from datetime import datetime
from collections import Counter
from typing import Optional

from sqlalchemy.orm import Session

from . import models


def get_gender_list():
    return [{"id": 8507, "name": "MALE"}, {"id": 8532, "name": "FEMALE"}]


def get_race_list():
    # race_list = [
    #     {"id": race.id, "name": race.concept_name}
    #     for race in db.query(models.Concept).filter_by(domain_id="Race").all()
    # ]

    # cleaned_race_list = []
    # for race in race_list:
    #     result = db.query(models.Person).filter_by(race_concept_id=race["id"]).first()
    #     if result != None:
    #         cleaned_race_list.append(race)
    cleaned_race_list = [
        {"id": 8515, "name": "Asian"},
        {"id": 8516, "name": "Black or African American"},
        {"id": 8527, "name": "White"},
    ]
    return cleaned_race_list


def get_ethnicity_list(db: Session):
    ethnicity_list = [
        {"id": ethnicity.id, "name": ethnicity.concept_name}
        for ethnicity in db.query(models.Concept).filter_by(domain_id="Ethnicity").all()
    ]
    return ethnicity_list


def get_all_person(db: Session):
    return db.query(models.Person).all()


def get_person_by_gender(db: Session):
    # gender_list = [gender.id for gender in db.query(models.Concept).filter_by(domain_id="Gender").all()]
    gender_list = get_gender_list()
    result = {}
    for gender in gender_list:
        count = len(db.query(models.Person).filter_by(gender_concept_id=gender["id"]).all())
        result |= {gender["name"]: count}
    return result


def get_person_by_race(db: Session):

    cleaned_race_list = get_race_list()
    result = {}
    for race in cleaned_race_list:
        count = len(db.query(models.Person).filter_by(race_concept_id=race["id"]).all())
        result |= {race["name"]: count}
    return result


def get_person_by_ethnicity(db: Session):
    ethnicity_list = get_ethnicity_list(db)
    result = {}
    for ethnicity in ethnicity_list:
        count = len(db.query(models.Person).filter_by(ethnicity_concept_id=ethnicity["id"]).all())
        result |= {ethnicity["name"]: count}
    return result


def get_all_death(db: Session):
    return db.query(models.Death).all()


def get_visit_by_concept(db: Session):
    """
    9201 : Inpatient Visit (입원)
    9202 : Outpatient Visit (외래)
    9203 : Emergency Room Visit (응급)
    """
    visit_concept_list = (
        {"id": 9201, "name": "Inpatient Visit"},
        {"id": 9202, "name": "Outpatient Visit"},
        {"id": 9203, "name": "Emergency Room Visit"},
    )
    result = {}
    for concept in visit_concept_list:
        count = len(db.query(models.VisitOccurrence).filter_by(visit_concept_id=concept["id"]).all())
        result |= {concept["name"]: count}
    return result


def get_visit_by_gender(db: Session):
    gender_list = get_gender_list()
    result = {}
    for gender in gender_list:
        count = len(
            db.query(models.VisitOccurrence).join(models.Person).filter_by(gender_concept_id=gender["id"]).all()
        )
        result |= {gender["name"]: count}
    return result


def get_visit_by_race(db: Session):
    race_list = get_race_list()
    result = {}
    for race in race_list:
        count = len(db.query(models.VisitOccurrence).join(models.Person).filter_by(race_concept_id=race["id"]).all())
        result |= {race["name"]: count}
    return result


def get_visit_by_ethnicity(db: Session):
    ethnicity_list = get_ethnicity_list(db)
    result = {}
    for ethnicity in ethnicity_list:
        count = len(
            db.query(models.VisitOccurrence).join(models.Person).filter_by(ethnicity_concept_id=ethnicity["id"]).all()
        )
        result |= {ethnicity["name"]: count}
    return result


def calculate_age_range(birthDate: datetime):
    currentDate = datetime.today().date()

    age = int(currentDate.year - birthDate.year)
    monthCheck = int(currentDate.month - birthDate.month)
    dayCheck = int(currentDate.day - birthDate.day)
    if monthCheck < 0:
        age = age - 1
    elif dayCheck < 0 and monthCheck == 0:
        age = age - 1

    return (age // 10) * 10


def get_visit_by_age_range(db: Session):
    queries = db.query(models.VisitOccurrence).join(models.Person)
    ages = list(map(lambda q: calculate_age_range(q.person.birth_datetime), queries))
    counter = dict(Counter(ages))

    return dict((x, y) for x, y in sorted(counter.items()))


def search_concepts(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    domain_id: Optional[models.DomainName] = None,
    concept_name: Optional[str] = None,
):
    queries = db.query(models.Concept)
    if domain_id is not None:
        queries = queries.filter(models.Concept.domain_id == domain_id)
    if concept_name is not None:
        queries = queries.filter(models.Concept.concept_name.like(f"%{concept_name}%"))
    result = queries.offset(skip).limit(limit).all()
    return result


def get_concept(db: Session, concept_id: int):
    result = db.query(models.Concept).filter(models.Concept.id == concept_id).first()
    return result


def search_people(db: Session, skip: int = 0, limit: int = 100):
    queries = db.query(models.Person)

    result = queries.offset(skip).limit(limit).all()
    return result
