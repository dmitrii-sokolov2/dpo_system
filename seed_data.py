import random
from datetime import date, timedelta
from app.database import SessionLocal, engine
from app import models, crud, schemas

# Создаем таблицы, если их нет
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

# --- СПИСКИ ДЛЯ ГЕНЕРАЦИИ ---
last_names = ["Иванов", "Смирнов", "Кузнецов", "Попов", "Васильев", "Петров", "Соколов", "Михайлов", "Новиков", "Федоров", "Морозов", "Волков", "Алексеев", "Лебедев", "Семенов"]
first_names = ["Александр", "Дмитрий", "Максим", "Сергей", "Андрей", "Алексей", "Артём", "Илья", "Кирилл", "Михаил", "Никита", "Матвей", "Роман", "Егор", "Иван"]
middle_names = ["Александрович", "Дмитриевич", "Сергеевич", "Андреевич", "Алексеевич", "Михайлович", "Иванович", "Петрович"]
orgs = ["ООО 'Вектор'", "АО 'Прогресс'", "ПАО 'Сбербанк'", "МБОУ СОШ №5", "ИП Смирнов", "ООО 'Ромашка'", "НИИ 'Технологии'", "ГБУЗ 'ГКБ №1'", "ООО 'СтройИнвест'"]
statuses = ["new", "new", "new", "pending_payment", "accepted", "rejected", "recalled", "new"] # "new" больше, чтобы было что обрабатывать

# Получаем все программы из базы
programs = db.query(models.Program).all()
if not programs:
    print("❌ Ошибка: Сначала добавьте хотя бы одну программу через админку или Swagger!")
    exit()

print("⏳ Генерируем тестовые заявления...")

# --- ГЕНЕРАЦИЯ ---
for i in range(40): # Количество заявок
    # 1. Генерируем случайного слушателя
    last = random.choice(last_names)
    first = random.choice(first_names)
    middle = random.choice(middle_names) if random.random() > 0.3 else None
    email = f"test_{random.randint(1000, 9999)}@example.com"
    phone = f"+79{random.randint(100000000, 999999999)}"
    snils = f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(100, 999)} 00"
    org = random.choice(orgs) if random.random() > 0.4 else None

    # Создаем слушателя
    listener_data = schemas.ListenerCreate(
        last_name=last, first_name=first, middle_name=middle,
        email=email, phone=phone, snils=snils, organization=org
    )
    listener = crud.create_listener(db, listener_data)

    # 2. Создаем заявление для него
    program = random.choice(programs)
    status = random.choice(statuses)
    comment = "Хочу повысить квалификацию" if random.random() > 0.5 else None
    
    app_data = schemas.ApplicationCreate(
        listener_id=listener.id,
        program_id=program.id,
        comment=comment
    )
    application = crud.create_application(db, app_data)
    
    # 3. Сразу меняем статус и дату (чтобы были разные)
    application.status = status
    # Рандомная дата за последние 30 дней
    application.created_at = date.today() - timedelta(days=random.randint(0, 30))
    
    db.commit()

print(f"✅ Успешно создано {40} заявлений с разными статусами!")
db.close()