from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class CategoryResponse(BaseModel):
    id: int
    name: str
    slug: str
    icon_url: str

    class Config:
        from_attributes = True


class IssueResponse(BaseModel):
    id: int
    title: str
    pdf_link: Optional[str]
    cover_image: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class ArticleAuthorResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class ArticleResponse(BaseModel):
    id: int
    title: str
    content: Optional[str]
    image_url: Optional[str]
    author: ArticleAuthorResponse
    category: CategoryResponse
    is_premium: bool
    published_at: datetime
    views_count: int
    likes_count: int

    class Config:
        from_attributes = True


class ArticleDetailResponse(BaseModel):
    id: int
    title: str
    content: str
    image_url: Optional[str]
    author: ArticleAuthorResponse
    category: CategoryResponse
    is_premium: bool
    published_at: datetime
    views_count: int
    likes_count: int

    class Config:
        from_attributes = True


class SavedArticleResponse(BaseModel):
    id: int
    article: ArticleResponse
    saved_at: datetime

    class Config:
        from_attributes = True


class PollResponse(BaseModel):
    id: int
    question: str
    options: List[str]
    results: dict
    article_id: Optional[int]

    class Config:
        from_attributes = True


class PollVoteRequest(BaseModel):
    selected_option: str


class ArticleCreateRequest(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None
    category_id: int
    issue_id: Optional[int] = None
    is_premium: bool = False


class ArticleUpdateRequest(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None
    category_id: Optional[int] = None
    issue_id: Optional[int] = None
    is_premium: Optional[bool] = None
