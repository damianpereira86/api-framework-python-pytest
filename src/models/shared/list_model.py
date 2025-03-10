from typing import Generic, List, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=[BaseModel])

class ListModel(BaseModel, Generic[T]):
    data: List[T]