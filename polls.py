from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from dependencies import db_dependency
from auth import get_user
import models
from schemas import PollResponse, PollVoteRequest
from typing import List, Optional


router = APIRouter(
    prefix='/polls',
    tags=['polls']
)


@router.get("/{poll_id}", response_model=PollResponse, status_code=status.HTTP_200_OK)
async def get_poll(
    poll_id: int,
    db: db_dependency
):
    """Отримати опитування"""
    poll = db.query(models.Poll).filter(models.Poll.id == poll_id).first()
    if poll is None:
        raise HTTPException(status_code=404, detail="Опитування не знайдено")
    
    return PollResponse(
        id=poll.id,
        question=poll.question,
        options=poll.options if poll.options else [],
        results=poll.results if poll.results else {},
        article_id=poll.article_id
    )


@router.post("/{poll_id}/vote", status_code=status.HTTP_200_OK)
async def vote_poll(
    poll_id: int,
    request: PollVoteRequest,
    db: db_dependency,
    user: dict = Depends(get_user)
):
    """Проголосувати в опитуванні"""
    poll = db.query(models.Poll).filter(models.Poll.id == poll_id).first()
    if poll is None:
        raise HTTPException(status_code=404, detail="Опитування не знайдено")
    
    existing_vote = db.query(models.PollVote).filter(
        models.PollVote.user_id == user['id'],
        models.PollVote.poll_id == poll_id
    ).first()
    
    if existing_vote:
        raise HTTPException(status_code=400, detail="Ви вже проголосували в цьому опитуванні")
    
    if poll.options and request.selected_option not in poll.options:
        raise HTTPException(status_code=400, detail="Обрана опція не існує")
    
    if poll.results is None:
        poll.results = {}
    
    if request.selected_option in poll.results:
        poll.results[request.selected_option] += 1
    else:
        poll.results[request.selected_option] = 1
    
    vote = models.PollVote(
        user_id=user['id'],
        poll_id=poll_id,
        selected_option=request.selected_option
    )
    
    db.add(vote)
    db.commit()
    db.refresh(poll)
    
    return {
        "message": "Голос зараховано",
        "results": poll.results
    }


