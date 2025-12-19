from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from typing import List
from datetime import datetime, timezone
from dependencies import db_dependency
from auth import get_user
import models
from schemas import SavedArticleResponse, ArticleResponse, ArticleAuthorResponse, CategoryResponse


router = APIRouter(
    prefix='/profile',
    tags=['profile']
)


@router.get('/main')
async def get_profile(user: dict = Depends(get_user), db: db_dependency = None):
    """Отримати інформацію про профіль користувача"""
    db_user = db.query(models.Users).filter(models.Users.id == user['id']).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")
    
    active_subscription = db.query(models.Subscription).filter(
        models.Subscription.user_id == user['id'],
        models.Subscription.is_active == True,
        models.Subscription.end_date > datetime.now(timezone.utc)
    ).first()
    
    is_premium = active_subscription is not None
    
    return {
        "user_id": db_user.id,
        "username": db_user.username,
        "email": db_user.email,
        "is_premium": is_premium
    }


@router.get('/bookmarks', response_model=List[SavedArticleResponse], status_code=status.HTTP_200_OK)
async def get_bookmarks(user: dict = Depends(get_user), db: db_dependency = None):
    """Отримати список збережених статей (закладок)"""
    user_id = user['id']
    saved_articles = db.query(models.SavedArticle).filter(
        models.SavedArticle.user_id == user_id
    ).order_by(models.SavedArticle.saved_at.desc()).all()
    
    result = []
    for saved in saved_articles:
        article = saved.article
        result.append(SavedArticleResponse(
            id=saved.id,
            article=ArticleResponse(
                id=article.id,
                title=article.title,
                content=article.content[:200] + "..." if len(article.content) > 200 else article.content,
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
            ),
            saved_at=saved.saved_at
        ))
    
    return result


@router.post('/bookmarks/{article_id}', status_code=status.HTTP_201_CREATED)
async def add_bookmark(
    article_id: int,
    user: dict = Depends(get_user),
    db: db_dependency = None
):
    """Додати статтю в закладки"""
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="Стаття не знайдена")
    
    existing = db.query(models.SavedArticle).filter(
        models.SavedArticle.user_id == user['id'],
        models.SavedArticle.article_id == article_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Стаття вже додана в закладки")
    
    saved_article = models.SavedArticle(
        user_id=user['id'],
        article_id=article_id
    )
    
    db.add(saved_article)
    db.commit()
    db.refresh(saved_article)
    
    return {"message": "Статтю додано в закладки", "saved_article_id": saved_article.id}


@router.delete('/bookmarks/{article_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_bookmark(
    article_id: int,
    user: dict = Depends(get_user),
    db: db_dependency = None
):
    """Видалити статтю з закладок"""
    saved_article = db.query(models.SavedArticle).filter(
        models.SavedArticle.user_id == user['id'],
        models.SavedArticle.article_id == article_id
    ).first()
    
    if saved_article is None:
        raise HTTPException(status_code=404, detail="Закладка не знайдена")
    
    db.delete(saved_article)
    db.commit()
    return None
