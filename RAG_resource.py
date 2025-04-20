from models import ChatRequest,ChatResponse
from fastapi import FastAPI, HTTPException,UploadFile,File
from RAG_service import RAGService
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import shutil

app = FastAPI(
    title="FST Chatbot API",
    description="API for the FST Chatbot",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)



service = RAGService()


import os

@app.get("/pdfs")
async def get_pdfs():
    """
    Returns a list of all PDF files in the knowledge base.
    
    Returns:
        list: A list of PDF filenames in the knowledge base.
    """
    try:
        # Get the path to the PDFs folder
        pdfs_folder = "knowledge_base_creation/pdfs"
        
        # Check if the folder exists
        if not os.path.exists(pdfs_folder):
            return []
        
        # Get all files in the folder with .pdf extension
        pdf_files = [f for f in os.listdir(pdfs_folder) if f.endswith('.pdf')]
        
        return {"pdf_files": pdf_files}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving PDF list: {str(e)}")




@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Handle chat requests from the user.
    
    Args:
        request (ChatRequest): The user's chat request containing the prompt and context.
        
    Returns:
        ChatResponse: The chatbot's response.
    """
    try:
        response = service.query_llm(request.user_prompt, request.context)
        
        return ChatResponse(response=response)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/upload")
async def upload_pdf(file : UploadFile  = File(...)):
    """
    Adds a PDF file to the knowledge base.
    
    Args:
        file (UploadFile): The PDF file to be uploaded.
        
    Returns:
        dict: A message indicating successful upload .
    """
    try:
        temp_dir = tempfile.mkdtemp()
        file_path = f"{temp_dir}/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        service.add_pdf(file_path)
        shutil.rmtree(temp_dir)
        return {"message": "File uploaded and processed successfully."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.delete("/delete")
async def delete_file(filename: str):
    """
    Deletes a file from the knowledge base.
    Args:
        filename (str): The name of the file to be deleted.
    Returns:
        dict: A message indicating successful deletion.
    """
    try:
        service.delete_pdf(filename)
        return {"message": "File deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


