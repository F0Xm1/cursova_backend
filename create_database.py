import os
from database import SessionLocal, engine
import models
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

db_file = "project.db"
if os.path.exists(db_file):
    os.remove(db_file)
    print(f"Видалено стару базу: {db_file}")

models.Base.metadata.create_all(bind=engine)
print("Створено нову базу даних")

db = SessionLocal()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

try:
    admin_user = models.Users(
        username="admin",
        email="admin@example.com",
        hashed_password=pwd_context.hash("Admin1234"),
        is_admin=True,
    )
    db.add(admin_user)
    
    test_user = models.Users(
        username="testuser",
        email="test@example.com",
        hashed_password=pwd_context.hash("Test1234"),
        is_admin=False,
    )
    db.add(test_user)
    
    premium_user = models.Users(
        username="premiumuser",
        email="premium@example.com",
        hashed_password=pwd_context.hash("Premium1234"),
        is_admin=False,
    )
    db.add(premium_user)
    
    db.commit()
    db.refresh(admin_user)
    db.refresh(test_user)
    db.refresh(premium_user)
    
    print("Створено користувачів: admin, testuser, premiumuser")

    categories_data = [
        {"name": "Спорт", "slug": "sport", "icon_url": "https://i.pinimg.com/736x/7f/91/2b/7f912b092e71134f0e7db187be68f37b.jpg"},
        {"name": "Мода", "slug": "fashion", "icon_url": "https://i.pinimg.com/736x/2f/89/5e/2f895ec7135aaca90a61ce2d86740e29.jpg"},
        {"name": "Технології", "slug": "tech", "icon_url": "https://i.pinimg.com/1200x/e1/22/34/e122343ac7ddb125851689e1fb05cc4a.jpg"},
        {"name": "Подорожі", "slug": "travel", "icon_url": "https://i.pinimg.com/736x/c2/b3/16/c2b3164fabf5f29edd61f324b907848a.jpg"},
        {"name": "Кулінарія", "slug": "food", "icon_url": "https://i.pinimg.com/736x/c8/a7/c3/c8a7c3a22a8f1e23c11bfe498146f2d6.jpg"},
        {"name": "Здоров'я", "slug": "health", "icon_url": "https://i.pinimg.com/736x/d7/e1/b3/d7e1b34aeb69ffc42b0b3016eee63723.jpg"},
        {"name": "Культура", "slug": "culture", "icon_url": "https://i.pinimg.com/1200x/a4/40/25/a440251511afa6bb597de01518ae567b.jpg"},
        {"name": "Бізнес", "slug": "business", "icon_url": "https://i.pinimg.com/736x/18/06/43/1806438b343308b261f3765342deaa74.jpg"},
    ]
    
    categories = []
    for cat_data in categories_data:
        category = models.Category(**cat_data)
        db.add(category)
        categories.append(category)
        print(f"Додано категорію: {cat_data['name']}")
    
    db.commit()

    for cat in categories:
        db.refresh(cat)
    
    category_dict = {cat.slug: cat for cat in categories}
    
    issues_data = [
        {"title": "Журнал Жовтень 2025", "cover_image": "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=400&q=80"},
        {"title": "Журнал Листопад 2025", "cover_image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&q=80"},
        {"title": "Журнал Грудень 2025", "cover_image": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400&q=80"},
    ]
    
    issues = []
    for issue_data in issues_data:
        issue = models.Issue(**issue_data)
        db.add(issue)
        issues.append(issue)
        print(f"Додано випуск: {issue_data['title']}")
    
    db.commit()
    
    for issue in issues:
        db.refresh(issue)
    
    articles_data = [
        {
            "title": "Топ-10 найкращих футбольних команд 2025",
            "content": "<h1>Топ-10 найкращих футбольних команд 2025</h1><p>У цій статті ми розглянемо найкращі футбольні команди світу...</p>",
            "image_url": "https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=800&q=80",
            "category_slug": "sport",
            "is_premium": False,
            "issue_id": 1
        },
        {
            "title": "Ексклюзив: Інтерв'ю з чемпіоном світу",
            "content": "<h1>Ексклюзивне інтерв'ю</h1><p>Ми зустрілися з чемпіоном світу...</p>",
            "image_url": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800&q=80",
            "category_slug": "sport",
            "is_premium": True,
            "issue_id": 1
        },
        {
            "title": "Тренди моди осінь-зима 2025",
            "content": "<h1>Тренди моди</h1><p>Що буде модно цієї осені та зими...</p>",
            "image_url": "https://images.unsplash.com/photo-1445205170230-053b83016050?w=800&q=80",
            "category_slug": "fashion",
            "is_premium": False,
            "issue_id": 1
        },
        {
            "title": "VIP: Колекція від відомого дизайнера",
            "content": "<h1>Ексклюзивна колекція</h1><p>Преміум контент про нову колекцію...</p>",
            "image_url": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=800&q=80",
            "category_slug": "fashion",
            "is_premium": True,
            "issue_id": 1
        },
        {
            "title": "Нові технології в смартфонах 2025",
            "content": "<h1>Технології майбутнього</h1><p>Огляд нових технологій...</p>",
            "image_url": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&q=80",
            "category_slug": "tech",
            "is_premium": False,
            "issue_id": 2
        },
        {
            "title": "Ексклюзив: Огляд нових iPhone",
            "content": "<h1>Детальний огляд</h1><p>Повний огляд нових iPhone...</p>",
            "image_url": "https://images.unsplash.com/photo-1523275126811-40c6e0e9b2b3?w=800&q=80",
            "category_slug": "tech",
            "is_premium": True,
            "issue_id": 2
        },
        {
            "title": "Найкращі місця для відпочинку взимку",
            "content": "<h1>Зимові подорожі</h1><p>Куди поїхати взимку...</p>",
            "image_url": "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=800&q=80",
            "category_slug": "travel",
            "is_premium": False,
            "issue_id": 2
        },
        {
            "title": "VIP: Приватні курорти для еліти",
            "content": "<h1>Ексклюзивні курорти</h1><p>Найрозкішніші місця для відпочинку...</p>",
            "image_url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80",
            "category_slug": "travel",
            "is_premium": True,
            "issue_id": 2
        },
        {
            "title": "Рецепти здорового харчування",
            "content": "<h1>Здорове харчування</h1><p>Корисні рецепти...</p>",
            "image_url": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800&q=80",
            "category_slug": "food",
            "is_premium": False,
            "issue_id": 3
        },
        {
            "title": "Ексклюзив: Рецепти від шеф-кухаря зірок",
            "content": "<h1>VIP рецепти</h1><p>Секретні рецепти від відомих кухарів...</p>",
            "image_url": "https://images.unsplash.com/photo-1556910103-1c02745aae4d?w=800&q=80",
            "category_slug": "food",
            "is_premium": True,
            "issue_id": 3
        },
        {
            "title": "Як підтримувати здоров'я взимку",
            "content": "<h1>Зимове здоров'я</h1><p>Поради для здорового способу життя...</p>",
            "image_url": "https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=800&q=80",
            "category_slug": "health",
            "is_premium": False,
            "issue_id": 3
        },
        {
            "title": "VIP: Персональна програма тренувань",
            "content": "<h1>Ексклюзивна програма</h1><p>Індивідуальна програма від тренера...</p>",
            "image_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=800&q=80",
            "category_slug": "health",
            "is_premium": True,
            "issue_id": 3
        },
    ]
    
    for article_data in articles_data:
        category = category_dict[article_data.pop("category_slug")]
        issue_id = article_data.pop("issue_id")
        
        article = models.Article(
            title=article_data["title"],
            content=article_data["content"],
            image_url=article_data["image_url"],
            author_id=admin_user.id,
            category_id=category.id,
            issue_id=issue_id,
            is_premium=article_data["is_premium"],
            published_at=datetime.now(timezone.utc)
        )
        db.add(article)
        print(f"Додано статтю: {article_data['title']}")
    
    db.commit()
    
    premium_subscription = models.Subscription(
        user_id=premium_user.id,
        type="monthly",
        start_date=datetime.now(timezone.utc),
        end_date=datetime.now(timezone.utc) + timedelta(days=30),
        is_active=True
    )
    db.add(premium_subscription)
    print("Створено premium підписку для premiumuser")
    
    db.commit()
    
    articles_list = db.query(models.Article).all()
    
    polls_data = [
        {
            "question": "Яка ваша улюблена категорія?",
            "options": ["Спорт", "Мода", "Технології", "Подорожі", "Кулінарія", "Здоров'я"],
            "article_id": None
        },
        {
            "question": "Чи читаєте ви premium статті?",
            "options": ["Так, регулярно", "Іноді", "Ні"],
            "article_id": articles_list[1].id if len(articles_list) > 1 else None
        },
        {
            "question": "Як часто ви читаєте статті на нашій платформі?",
            "options": ["Щодня", "Кілька разів на тиждень", "Раз на тиждень", "Рідко"],
            "article_id": None
        },
        {
            "question": "Яка найважливіша функція для вас?",
            "options": ["Закладки", "Premium контент", "Опитування", "Категорії"],
            "article_id": None
        },
        {
            "question": "Чи подобається вам формат журнальних випусків?",
            "options": ["Так, дуже", "Так, непогано", "Нейтрально", "Не подобається"],
            "article_id": articles_list[0].id if len(articles_list) > 0 else None
        },
        {
            "question": "Яку тему ви хочете бачити частіше?",
            "options": ["Спорт", "Технології", "Мода", "Подорожі", "Здоров'я", "Кулінарія"],
            "article_id": None
        },
        {
            "question": "Як ви оцінюєте якість контенту?",
            "options": ["Відмінно", "Добре", "Задовільно", "Погано"],
            "article_id": articles_list[2].id if len(articles_list) > 2 else None
        },
        {
            "question": "Чи готові ви платити за premium підписку?",
            "options": ["Так, вже плачу", "Так, планую", "Можливо", "Ні"],
            "article_id": None
        },
        {
            "question": "Як ви переважно читаєте статті?",
            "options": ["На комп'ютері", "На планшеті", "На смартфоні", "Не має значення"],
            "article_id": None
        },
        {
            "question": "Що вас найбільше цікавить в статтях?",
            "options": ["Ексклюзивні інтерв'ю", "Практичні поради", "Огляди та рейтинги", "Новини та тренди"],
            "article_id": articles_list[3].id if len(articles_list) > 3 else None
        },
    ]
    
    for poll_data in polls_data:
        poll = models.Poll(**poll_data)
        db.add(poll)
        print(f"Додано опитування: {poll_data['question']}")
    
    db.commit()
    
    print("\nБаза даних успішно створена!")
    print("\nТестові користувачі:")
    print("  - admin / Admin1234 (адміністратор)")
    print("  - testuser / Test1234 (звичайний користувач)")
    print("  - premiumuser / Premium1234 (premium користувач)")
    
except Exception as e:
    db.rollback()
    print(f"Помилка при створенні бази даних: {e}")
    raise
finally:
    db.close()
