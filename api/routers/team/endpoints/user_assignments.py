from logging import getLogger
from uuid import UUID
from typing import Optional

from fastapi import APIRouter, Depends, Query

from services.team_services import TeamService
from schemas.team import TeamUsersResponse
from core.dependencies import get_team_service


router = APIRouter(tags=["Assignments"])
logger = getLogger(__name__)


@router.get("/{team_id}/users", response_model=TeamUsersResponse, tags=["Get Assignments"])
async def get_team_users(
    team_id: UUID,
    hunting_year_id: Optional[UUID] = Query(
        None, description="ID of the hunting year"),
    team_service: TeamService = Depends(get_team_service)
):

    users, hunting_year = await team_service.get_users_for_hunting_team_and_year(team_id, hunting_year_id)
    return TeamUsersResponse(
        hunting_year=hunting_year,
        users=users
    )