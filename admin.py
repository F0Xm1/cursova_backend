from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from sqlalchemy.orm import Session
from dependencies import db_dependency, get_db
from auth import get_user
import models
from schemas import ArticleCreateRequest, ArticleUpdateRequest, ArticleResponse, ArticleAuthorResponse, CategoryResponse


router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)


def _require_admin(user: dict = Depends(get_user), db: Session = Depends(get_db)):
    """Перевірка прав адміністратора"""
    db_user = db.query(models.Users).filter(models.Users.id == user["id"]).first()
    if not db_user or not db_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Потрібен доступ адміністратора")
    return db_user


@router.post("/articles", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
async def create_article(
    payload: ArticleCreateRequest,
    db: db_dependency,
    admin: models.Users = Depends(_require_admin)
):
    """Створити нову статтю"""
    category = db.query(models.Category).filter(models.Category.id == payload.category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Категорія не знайдена")
    
    if payload.issue_id:
        issue = db.query(models.Issue).filter(models.Issue.id == payload.issue_id).first()
        if issue is None:
            raise HTTPException(status_code=404, detail="Випуск не знайдено")
    
    article = models.Article(
        title=payload.title,
        content=payload.content,
        image_url=payload.image_url,
        author_id=admin.id,
        category_id=payload.category_id,
        issue_id=payload.issue_id,
        is_premium=payload.is_premium
    )
    
    db.add(article)
    db.commit()
    db.refresh(article)
    
    return ArticleResponse(
        id=article.id,
        title=article.title,
        content=article.content,
        image_url=article.image_url,
        author=ArticleAuthorResponse(id=article.author.id, username=article.author.username),
        category=CategoryResponse(
            id=article.category.id,
            name=article.category.name,
            slug=article.category.slug,
            icon_url=article.category.icon_url
        ),
        is_premium=article.is_premium,
        published_at=article.published_at,
        views_count=article.views_count,
        likes_count=article.likes_count
    )


@router.put("/articles/{article_id}", response_model=ArticleResponse, status_code=status.HTTP_200_OK)
async def update_article(
    article_id: int,
    payload: ArticleUpdateRequest,
    db: db_dependency,
    admin: models.Users = Depends(_require_admin)
):
    """Редагувати статтю"""
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if article is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Стаття не знайдена")
    
    update_data = payload.model_dump(exclude_none=True)
    
    if 'category_id' in update_data:
        category = db.query(models.Category).filter(models.Category.id == update_data['category_id']).first()
        if category is None:
            raise HTTPException(status_code=404, detail="Категорія не знайдена")
    
    if 'issue_id' in update_data and update_data['issue_id']:
        issue = db.query(models.Issue).filter(models.Issue.id == update_data['issue_id']).first()
        if issue is None:
            raise HTTPException(status_code=404, detail="Випуск не знайдено")
    
    for field, value in update_data.items():
        setattr(article, field, value)
    
    db.commit()
    db.refresh(article)
    
    return ArticleResponse(
        id=article.id,
        title=article.title,
        content=article.content,
        image_url=article.image_url,
        author=ArticleAuthorResponse(id=article.author.id, username=article.author.username),
        category=CategoryResponse(
            id=article.category.id,
            name=article.category.name,
            slug=article.category.slug,
            icon_url=article.category.icon_url
        ),
        is_premium=article.is_premium,
        published_at=article.published_at,
        views_count=article.views_count,
        likes_count=article.likes_count
    )


@router.delete("/articles/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(
    article_id: int,
    db: db_dependency,
    admin: models.Users = Depends(_require_admin)
):
    """Видалити статтю"""
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if article is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Стаття не знайдена")
    
    db.delete(article)
    db.commit()
    return None


@router.get("/articles", response_model=list[ArticleResponse], status_code=status.HTTP_200_OK)
async def list_articles(
    db: db_dependency,
    admin: models.Users = Depends(_require_admin)
):
    """Отримати список всіх статей (для адміністратора)"""
    articles = db.query(models.Article).order_by(models.Article.published_at.desc()).all()
    
    result = []
    for article in articles:
        result.append(ArticleResponse(
            id=article.id,
            title=article.title,
            content=article.content,
            image_url=article.image_url,
            author=ArticleAuthorResponse(id=article.author.id, username=article.author.username),
            category=CategoryResponse(
                id=article.category.id,
                name=article.category.name,
                slug=article.category.slug,
                icon_url=article.category.icon_url
            ),
            is_premium=article.is_premium,
            published_at=article.published_at,
            views_count=article.views_count,
            likes_count=article.likes_count
        ))
    
    return result
