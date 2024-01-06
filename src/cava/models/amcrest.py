from pydantic import BaseModel, Field


class event(BaseModel):
    code: str = Field(alias="Code")
    action: str
    index: int
    camera: str

    def ttl(self):
        return 600  # 600 Seconds
