from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from appie.core.database import get_db
from appie.schemas.schemas import Module, ModuleCreate
from appie.crud.crud_module import get_user_modules, create_user_module

router = APIRouter()

@router.post("/modules/", response_model=Module)
def create_module(module: ModuleCreate, user_id: str, db: Session = Depends(get_db)):
    return create_user_module(db=db, module=module, user_id=user_id)

@router.get("/users/{user_id}/modules", response_model=List[Module])
def read_user_modules(user_id: str, db: Session = Depends(get_db)):
    modules = get_user_modules(db, user_id=user_id)
    return modules