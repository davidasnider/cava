from pydantic import BaseModel
from typing import Optional


class event(BaseModel):
    code: Optional[str]
    action: Optional[str]
    index: Optional[int]
    camera: Optional[str]

    def ttl(self):
        return 600  # 600 Seconds
