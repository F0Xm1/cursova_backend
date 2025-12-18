from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
import random
from dependencies import db_dependency
from auth import get_user
import models
from schemas import (
    ArticleResponse,
    ArticleDetailResponse,
    CategoryResponse,
    ArticleAuthorResponse
)
from datetime import datetime, timezone


router = APIRouter(
    prefix='/articles',
    tags=['articles']
)


def check_premium_access(user: Optional[dict], db: Session) -> bool:
    """Перевіряє чи є у користувача активна premium підписка"""
    if user is None:
        return False
    
    active_subscription = db.query(models.Subscription).filter(
        models.Subscription.user_id == user['id'],
        models.Subscription.is_active == True,
        models.Subscription.end_date > datetime.now(timezone.utc)
    ).first()
    
    return active_subscription is not None


@router.get("/all", response_model=List[ArticleResponse], status_code=status.HTTP_200_OK)
async def get_all_articles_random(
    db: db_dependency,
    user: Optional[dict] = Depends(get_user)
):
    """Отримати всі статті у рандомному порядку"""
    articles = db.query(models.Article).all()

    random.shuffle(articles)
    
    has_premium = check_premium_access(user, db)
    
    result = []
    for article in articles:
        content = article.content
        if article.is_premium and not has_premium:
            content = article.content[:200] + "..." if len(article.content) > 200 else article.content
        
        result.append(ArticleResponse(
            id=article.id,
            title=article.title,
            content=content,
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


@router.get("", response_model=List[ArticleResponse], status_code=status.HTTP_200_OK)
async def get_articles(
    db: db_dependency,
    category: Optional[str] = Query(None, description="Slug категорії (sport, fashion, etc.)"),
    sort: Optional[str] = Query(None, description="Сортування: popular, recent"),
    page: int = Query(1, ge=1, description="Номер сторінки"),
    user: Optional[dict] = Depends(get_user)
):
    """Отримати список статей з фільтрацією та сортуванням"""
    query = db.query(models.Article)
    
    if category:
        category_obj = db.query(models.Category).filter(models.Category.slug == category).first()
        if category_obj:
            query = query.filter(models.Article.category_id == category_obj.id)
        else:
            raise HTTPException(status_code=404, detail=f"Категорія '{category}' не знайдена")
    
    if sort == 'popular':
        query = query.order_by(models.Article.views_count.desc(), models.Article.likes_count.desc())
    elif sort == 'recent':
        query = query.order_by(models.Article.published_at.desc())
    else:
        query = query.order_by(models.Article.published_at.desc())
    
    page_size = 10
    offset = (page - 1) * page_size
    articles = query.offset(offset).limit(page_size).all()
    
    has_premium = check_premium_access(user, db)
    
    result = []
    for article in articles:
        content = article.content
        if article.is_premium and not has_premium:
            content = article.content[:200] + "..." if len(article.content) > 200 else article.content
        
        result.append(ArticleResponse(
            id=article.id,
            title=article.title,
            content=content,
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


@router.get("/{article_id}", response_model=ArticleDetailResponse)
async def get_article_details(
    article_id: int,
    db: db_dependency,
    user: Optional[dict] = Depends(get_user)
):
    """Отримати детальну інформацію про статтю"""
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="Стаття не знайдена")
    
    has_premium = check_premium_access(user, db)
    
    if article.is_premium and not has_premium:
        raise HTTPException(
            status_code=403,
            detail="Ця стаття доступна тільки для premium користувачів. Будь ласка, придбайте підписку."
        )
    
    article.views_count += 1
    db.commit()
    db.refresh(article)
    
    return ArticleDetailResponse(
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


@router.post("/{article_id}/like", status_code=status.HTTP_200_OK)
async def like_article(
    article_id: int,
    db: db_dependency,
    user: dict = Depends(get_user)
):
    """Лайкнути статтю"""
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="Стаття не знайдена")
    
    article.likes_count += 1
    db.commit()
    db.refresh(article)
    
    return {"message": "Статтю лайкнуто", "likes_count": article.likes_count}


@router.get("/categories/list", response_model=List[CategoryResponse], status_code=status.HTTP_200_OK)
async def get_categories(db: db_dependency):
    """Отримати список категорій для меню"""
    categories = db.query(models.Category).all()
    return categories
