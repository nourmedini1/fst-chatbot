from langchain_huggingface import HuggingFaceEmbeddings
from config import Config
import logging
import os
from knowledge_base_creation.PDF_processor import PDFProcessor
from knowledge_base_creation.document_generator import DocumentGenerator
from knowledge_base_creation.vector_store_manager import VectorStoreManager

class KnowledgeBaseCreationPipeline:
    """
    A class to create a knowledge base using LangChain.
    """ 
    def __init__(self, PDFs_folder_path: str):
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Using device: {Config.DEVICE}")
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=Config.MODEL_NAME,
            model_kwargs={'device': Config.DEVICE},
            encode_kwargs={'normalize_embeddings': True}
        )
        self.pdf_processor = PDFProcessor(PDFs_folder_path)
        self.document_generator = DocumentGenerator()
        self.vector_store_manager = VectorStoreManager(self.embedding_model)
        self.logger.info("KnowledgeBaseCreationPipeline initialized successfully")

    def execute(self) : 
        """
        Creates embeddings for all PDFs in the given folder path.
        """
        self.logger.info("Creating embeddings for all PDFs...")
        for pdffile in os.listdir(self.pdf_processor.pdf_folder_path):
            if pdffile.endswith('.pdf'):
                pdf_path = os.path.join(self.pdf_processor.pdf_folder_path, pdffile)
                extracted_pdf_data = self.pdf_processor.process_pdf(pdf_path)
                if not extracted_pdf_data:
                    self.logger.warning(f"No data extracted from {pdffile}. Skipping...")
                    continue
                documents = self.document_generator.generate_documents(
                    extracted_pdf_data['text'], 
                    extracted_pdf_data['metadata']  
                )
                if not documents:
                    self.logger.warning(f"No documents generated from {pdffile}. Skipping...")
                    continue
                if not self.vector_store_manager.add_documents(documents, pdffile):
                    self.logger.error(f"Failed to add documents for {pdffile}.")
                    continue
                self.logger.info(f"Successfully created embeddings for {pdffile}.")
                self.logger.info(f"Stored document IDs for {pdffile} in local storage.")
                self.logger.info(f"Stored {len(documents)} documents for {pdffile} in the vector store.")
                self.vector_store_manager.persist_vector_store()


