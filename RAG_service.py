from  knowledge_base_creation.vector_store_manager import VectorStoreManager
from llm_client import LLMClient
from prompt_templates import create_reformulation_prompt,create_query_prompt
from knowledge_base_creation.PDF_processor import PDFProcessor
from knowledge_base_creation.document_generator import DocumentGenerator
from knowledge_base_creation.config import Config
from langchain_huggingface import HuggingFaceEmbeddings

class RAGService : 
    def __init__(self):
        self.vector_store_manager = VectorStoreManager(embedding_model=HuggingFaceEmbeddings(
            model_name=Config.MODEL_NAME,
            model_kwargs={'device': Config.DEVICE},
            encode_kwargs={'normalize_embeddings': True}
            )
        )
        self.llm_client = LLMClient("http://192.168.1.152:8000")
        self.pdf_processor = PDFProcessor("knowledge_base_creation/pdfs")
        self.document_generator = DocumentGenerator()

    
    def query_llm(self, user_prompt: str,context : str) -> str:
        """
        Query the LLM with a given question and return the answer.
        
        Args:
            query (str): The question to ask the LLM.
            
        Returns:
            str: The answer from the LLM.
        """
        try:
            reformalation_prompt = create_reformulation_prompt(user_prompt)
            reformulated_user_prompt = self.llm_client.get_response(reformalation_prompt)
            # Search for relevant documents in the vector store
            documents = self.vector_store_manager.search_documents(reformulated_user_prompt, k=5)
            llm_prompt = create_query_prompt(user_prompt, documents)
            response = self.llm_client.get_response(llm_prompt)
            return response
        except Exception as e:
            print(f"Error querying LLM: {e}")
            return "An error occurred while querying the LLM."
        

    def add_pdf(self, file_path: str):
        """
        Process a PDF file and add its content to the vector store.
        
        Args:
            file_path (str): The path to the PDF file.
        """
        try:
            result = self.pdf_processor.process_pdf(file_path)
            docs = self.document_generator.generate_documents(result['text'],result['metadata'])
            self.vector_store_manager.add_documents(docs,file_path)
        except Exception as e:
            print(f"Error processing PDF: {e}")

    def delete_pdf(self, filename: str):
        """
        Delete the embeddigns related to a PDF file from the vector store.
        
        Args:
            file_path (str): The path to the PDF file.
        """
        try:
            self.vector_store_manager.delete_documents(filename)
        except Exception as e:
            print(f"Error deleting PDF: {e}")

        