from typing import Annotated

from fastapi import APIRouter, Depends

from app.models import AuthenticatedUser
from app.routers.auth import get_current_user
from app.utils import db_dependency

recommendation_router = APIRouter()
user_dependency = Annotated[AuthenticatedUser, Depends(get_current_user)]


@recommendation_router.get('default_recommend')
def default_recommend(db: db_dependency):
    pass


@recommendation_router.get('user_recommend')
def user_recommend(user_id: user_dependency, db: db_dependency):
    pass
