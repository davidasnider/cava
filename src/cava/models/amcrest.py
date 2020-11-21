from pydantic import BaseModel
from typing import List, Optional


class event(BaseModel):
    code: Optional[str]
    action: Optional[str]
    index: Optional[int]
    camera: Optional[str]
