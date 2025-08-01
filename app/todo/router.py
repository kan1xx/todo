from typing import Annotated
from fastapi import APIRouter, Depends

from app.todo.repository import *
from app.todo.shemas import *


router = APIRouter(
    prefix='/tasks',
    tags=['Tasks']
)


@router.post('/add_task')
async def add_task(task: Annotated[STaskAdd, Depends()]) -> STaskId:
    task_id = await TaskRepository.add_one(task)
    return STaskId(id=task_id)


@router.get('/')
async def get_tasks() -> list[STask]:
    tasks = await TaskRepository.find_all()
    return tasks

@router.patch('update/{task_id}')
async def update_task(task_id: int,
                      update_data: STaskUpdate,
                      task: Annotated[STaskUpdate, Depends()]) -> STaskUpdate:
    updated_task = await TaskRepository.update_task(
        task,
        task_id=task_id,
        **update_data.model_dump(exclude_unset=True),
        
    )
    return updated_task


@router.delete('delete/{task_id}')
async def delete_task(task_id: int): 
    deleted_task = await TaskRepository.delete_task(
        task_id=task_id,

    )
    return deleted_task
