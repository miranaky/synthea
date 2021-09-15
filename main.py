from dataclasses import asdict
from typing import List, Optional
from fastapi.params import Depends
from sqlalchemy.orm.session import Session

from fastapi import FastAPI, HTTPException

from database import schemas, crud, models
from config import conf, settings
from database.database import db


config = conf()
conf_dict = asdict(config)

app = FastAPI()
db.init_app(app, **conf_dict)


@app.get("/static/person")
def read_person_info(db: Session = Depends(db.session)):
    total_person = crud.get_all_person(db)
    person_by_gender = crud.get_person_by_gender(db)
    person_by_race = crud.get_person_by_race(db)
    person_by_ethnicity = crud.get_person_by_ethnicity(db)
    total_death = crud.get_all_death(db)

    result = {
        "Total Patient": len(total_person),
        "Patient by Gender": person_by_gender,
        "Patient by Race": person_by_race,
        "Patient by Ethnicity": person_by_ethnicity,
        "Total Death": len(total_death),
    }

    return result


@app.get("/static/visit")
def read_visit_info(db: Session = Depends(db.session)):
    visit_by_concept = crud.get_visit_by_concept(db)
    visit_by_gender = crud.get_visit_by_gender(db)
    visit_by_race = crud.get_visit_by_race(db)
    visit_by_ethnicity = crud.get_visit_by_ethnicity(db)
    visit_by_age_range = crud.get_visit_by_age_range(db)

    result = {
        "Visit by concept": visit_by_concept,
        "visit_by_gender": visit_by_gender,
        "visit_by_race": visit_by_race,
        "visit_by_ethnicity": visit_by_ethnicity,
        "visit_by_age_range": visit_by_age_range,
    }

    return result


@app.get("/concepts/", response_model=List[schemas.Concept])
def read_concepts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(db.session),
    domain_id: Optional[models.DomainName] = None,
    concept_name: Optional[str] = None,
):
    concepts = crud.search_concepts(db, skip=skip, limit=limit, domain_id=domain_id, concept_name=concept_name)
    if len(concepts) <= 0:
        raise HTTPException(status_code=404, detail="Not found")

    return concepts


@app.get("/concepts/{concept_id}", response_model=schemas.Concept)
def read_concept(concept_id: int, db: Session = Depends(db.session)):
    db_concept = crud.get_concept(db, concept_id=concept_id)
    if db_concept is None:
        raise HTTPException(status_code=404, detail="Concept id not found")
    return db_concept


@app.get("/person/")
def read_people(skip: int = 0, limit: int = 100, db: Session = Depends(db.session)):
    people = crud.search_people(db, skip=skip, limit=limit)
    if len(people) <= 0:
        raise HTTPException(status_code=404, detail="Not found")
    return people
