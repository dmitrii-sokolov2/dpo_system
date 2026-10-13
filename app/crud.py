from sqlalchemy.orm import Session
from . import models, schemas
from datetime import date


def create_program(db: Session, data: schemas.ProgramCreate):
    program = models.Program(**data.dict())
    db.add(program)
    db.commit()
    db.refresh(program)
    return program


def get_programs(db: Session):
    return db.query(models.Program).all()


def create_listener(db: Session, data: schemas.ListenerCreate):
    listener = models.Listener(**data.dict())
    db.add(listener)
    db.commit()
    db.refresh(listener)
    return listener


def get_listeners(db: Session):
    return db.query(models.Listener).all()


def create_application(db: Session, data: schemas.ApplicationCreate):
    application = models.Application(
        listener_id=data.listener_id,
        program_id=data.program_id,
        comment=data.comment,
        status="new",
        created_at=date.today()
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


def get_applications(db: Session):
    return db.query(models.Application).all()


def update_application_status(db: Session, application_id: int, status: str):
    application = db.query(models.Application).filter(
        models.Application.id == application_id
    ).first()
    if application:
        application.status = status
        db.commit()
        db.refresh(application)
    return application