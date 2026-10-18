from fastapi import FastAPI, Depends, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import date

from . import models, schemas, crud
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Система документооборота ДПО")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    programs = crud.get_programs(db)
    listeners = crud.get_listeners(db)
    applications = crud.get_applications(db)
    return templates.TemplateResponse(
        request=request, name="index.html",
        context={"programs": programs, "listeners": listeners, "applications": applications, "active_page": "home"}
    )

@app.get("/apply", response_class=HTMLResponse)
def apply_form(request: Request, db: Session = Depends(get_db)):
    programs = crud.get_programs(db)
    return templates.TemplateResponse(
        request=request, name="apply.html",
        context={"programs": programs, "active_page": "apply"}
    )

@app.post("/apply")
def apply_submit(
    last_name: str = Form(...),
    first_name: str = Form(...),
    middle_name: str = Form(None),
    email: str = Form(...),
    phone: str = Form(None),
    snils: str = Form(None),
    organization: str = Form(None),
    program_id: int = Form(...),
    comment: str = Form(None),
    db: Session = Depends(get_db)
):
    existing_listener = db.query(models.Listener).filter(models.Listener.email == email).first()
    
    if existing_listener:
        listener = existing_listener
    else:
        new_listener_data = schemas.ListenerCreate(
            last_name=last_name, first_name=first_name, middle_name=middle_name,
            email=email, phone=phone, snils=snils, organization=organization
        )
        listener = crud.create_listener(db, new_listener_data)

    new_app_data = schemas.ApplicationCreate(
        listener_id=listener.id, program_id=program_id, comment=comment
    )
    application = crud.create_application(db, new_app_data)

    return RedirectResponse(url="/admin", status_code=303)

@app.get("/apply/success/{app_id}", response_class=HTMLResponse)
def apply_success(request: Request, app_id: int, db: Session = Depends(get_db)):
    application = db.query(models.Application).filter(models.Application.id == app_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Заявление не найдено")
    
    return templates.TemplateResponse(
        request=request,
        name="success.html",
        context={"application": application}
    )

@app.get("/admin", response_class=HTMLResponse)
def admin_panel(request: Request, db: Session = Depends(get_db)):
    applications = crud.get_applications(db)
    programs = crud.get_programs(db)
    
    # Считаем статистику
    total_apps = len(applications)
    new_apps = sum(1 for a in applications if a.status == 'new')
    accepted_apps = sum(1 for a in applications if a.status == 'accepted')
    rejected_apps = sum(1 for a in applications if a.status == 'rejected')
    
    for app in applications:
        app.listener_name = f"{app.listener.last_name} {app.listener.first_name}"
        app.program_name = app.program.name

    return templates.TemplateResponse(
        request=request, name="admin.html",
        context={
            "applications": applications, 
            "programs": programs, 
            "active_page": "admin",
            "stats": {
                "total": total_apps,
                "new": new_apps,
                "accepted": accepted_apps,
                "rejected": rejected_apps
            }
        }
    )

@app.post("/admin/update-status/{app_id}")
def admin_update_status(app_id: int, new_status: str = Form(...), db: Session = Depends(get_db)):
    crud.update_application_status(db, app_id, new_status)
    return RedirectResponse(url="/admin", status_code=303)

@app.post("/api/programs/", response_model=schemas.ProgramOut)
def create_program(data: schemas.ProgramCreate, db: Session = Depends(get_db)):
    return crud.create_program(db, data)

@app.get("/api/programs/", response_model=list[schemas.ProgramOut])
def list_programs(db: Session = Depends(get_db)):
    return crud.get_programs(db)

@app.post("/api/listeners/", response_model=schemas.ListenerOut)
def create_listener_api(data: schemas.ListenerCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Listener).filter(models.Listener.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Слушатель с таким email уже существует")
    return crud.create_listener(db, data)

@app.get("/api/listeners/", response_model=list[schemas.ListenerOut])
def list_listeners(db: Session = Depends(get_db)):
    return crud.get_listeners(db)

@app.post("/api/applications/", response_model=schemas.ApplicationOut)
def create_application_api(data: schemas.ApplicationCreate, db: Session = Depends(get_db)):
    return crud.create_application(db, data)

@app.get("/api/applications/", response_model=list[schemas.ApplicationOut])
def list_applications(db: Session = Depends(get_db)):
    return crud.get_applications(db)

@app.patch("/api/applications/{application_id}/status")
def update_status(application_id: int, status: str, db: Session = Depends(get_db)):
    return crud.update_application_status(db, application_id, status)