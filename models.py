from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_prompt: str
    context: list[str]

class ChatResponse(BaseModel) : 
    response : str