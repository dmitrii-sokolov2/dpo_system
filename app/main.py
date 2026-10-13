from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi import HTTPException

from . import models, schemas, crud
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Система документооборота ДПО")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    programs = crud.get_programs(db)
    applications = crud.get_applications(db)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "programs": programs,
            "applications": applications
        }
    )


@app.post("/api/programs/", response_model=schemas.ProgramOut)
def create_program(data: schemas.ProgramCreate, db: Session = Depends(get_db)):
    return crud.create_program(db, data)


@app.get("/api/programs/", response_model=list[schemas.ProgramOut])
def list_programs(db: Session = Depends(get_db)):
    return crud.get_programs(db)


@app.post("/api/listeners/", response_model=schemas.ListenerOut)
def create_listener(data: schemas.ListenerCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Listener).filter(
        models.Listener.email == data.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Слушатель с email {data.email} уже существует"
        )

    return crud.create_listener(db, data)


@app.get("/api/listeners/", response_model=list[schemas.ListenerOut])
def list_listeners(db: Session = Depends(get_db)):
    return crud.get_listeners(db)


@app.post("/api/applications/", response_model=schemas.ApplicationOut)
def create_application(data: schemas.ApplicationCreate, db: Session = Depends(get_db)):
    return crud.create_application(db, data)


@app.get("/api/applications/", response_model=list[schemas.ApplicationOut])
def list_applications(db: Session = Depends(get_db)):
    return crud.get_applications(db)


@app.patch("/api/applications/{application_id}/status")
def update_status(application_id: int, status: str, db: Session = Depends(get_db)):
    return crud.update_application_status(db, application_id, status)