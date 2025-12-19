from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from datetime import datetime, timedelta, timezone
from dependencies import db_dependency
from auth import get_user
import models
from schemas import SubscriptionBuyRequest, SubscriptionResponse


router = APIRouter(
    prefix='/subscription',
    tags=['subscription']
)


@router.post("/buy", response_model=SubscriptionResponse, status_code=status.HTTP_201_CREATED)
async def buy_subscription(
    request: SubscriptionBuyRequest,
    db: db_dependency,
    user: dict = Depends(get_user)
):
    """Придбати підписку"""
    if request.type not in ['monthly', 'yearly']:
        raise HTTPException(
            status_code=400,
            detail="Тип підписки повинен бути 'monthly' або 'yearly'"
        )
    
    existing_subscriptions = db.query(models.Subscription).filter(
        models.Subscription.user_id == user['id'],
        models.Subscription.is_active == True
    ).all()
    
    for sub in existing_subscriptions:
        sub.is_active = False
    
    start_date = datetime.now(timezone.utc)
    if request.type == 'monthly':
        end_date = start_date + timedelta(days=30)
    else:
        end_date = start_date + timedelta(days=365)
    
    subscription = models.Subscription(
        user_id=user['id'],
        type=request.type,
        start_date=start_date,
        end_date=end_date,
        is_active=True
    )
    
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    
    return SubscriptionResponse(
        id=subscription.id,
        type=subscription.type,
        start_date=subscription.start_date,
        end_date=subscription.end_date,
        is_active=subscription.is_active
    )


@router.get("/status", response_model=SubscriptionResponse, status_code=status.HTTP_200_OK)
async def get_subscription_status(
    db: db_dependency,
    user: dict = Depends(get_user)
):
    """Отримати статус поточної підписки"""
    subscription = db.query(models.Subscription).filter(
        models.Subscription.user_id == user['id'],
        models.Subscription.is_active == True,
        models.Subscription.end_date > datetime.now(timezone.utc)
    ).first()
    
    if subscription is None:
        raise HTTPException(status_code=404, detail="Активна підписка не знайдена")
    
    return SubscriptionResponse(
        id=subscription.id,
        type=subscription.type,
        start_date=subscription.start_date,
        end_date=subscription.end_date,
        is_active=subscription.is_active
    )


