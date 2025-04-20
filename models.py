from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_prompt: str
    context: str

class ChatResponse(BaseModel) : 
    response : str