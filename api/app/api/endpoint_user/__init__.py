import logging
from fastapi import APIRouter, Depends

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/{number}")
async def read_root(number: int):
    logger.debug(f'User passed the number: {number} at the route /')
    
    return numbers[number]