from config import Config
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import logging


class DocumentGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        try:
            self.splitter = RecursiveCharacterTextSplitter(
                chunk_size=Config.CHUNK_SIZE,
                chunk_overlap=Config.CHUNK_OVERLAP,
                length_function=len,
                separators=["\n\n", "\n", " ", ""]
            )
            self.logger.info("Document generator initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize text splitter: {e}")
            raise


    def split_text(self, text: str) -> List[str]:
        """Split the input text into chunks of size `self.chunk_size` with an overlap of `
        self.chunk_overlap`.
        Args:
            text (str): The input text to be chunked.
        Returns:
            List[str]: A list of chunked text strings.
        """
        try:
            if not text or not isinstance(text, str):
                self.logger.warning(f"Invalid text provided for splitting: {type(text)}")
                return []
                
            chunks = self.splitter.split_text(text)
            self.logger.debug(f"Split text into {len(chunks)} chunks")
            return chunks
        except Exception as e:
            self.logger.error(f"Error splitting text: {e}")
            return []
    

    def generate_documents(self, text: str, metadata: dict) -> List[Document]:
        """Generate documents from the input text and metadata.
        Args:
            text (str): The input text to be chunked.
            metadata (dict): Metadata associated with the text.
        Returns:
            List[Document]: A list of Document objects.
        """
        try:
            if not text:
                self.logger.warning("Empty text provided for document generation")
                return []
                
            if not isinstance(metadata, dict):
                self.logger.warning("Invalid metadata provided (not a dictionary)")
                metadata = {}
                
            chunks = self.split_text(text)
            if not chunks:
                self.logger.warning("No chunks generated from text")
                return []
                
            documents = []
            for chunk in chunks:
                try:
                    documents.append(Document(page_content=chunk, metadata=metadata))
                except Exception as e:
                    self.logger.error(f"Error creating document from chunk: {e}")
            
            self.logger.debug(f"Generated {len(documents)} documents")
            return documents
        except Exception as e:
            self.logger.error(f"Error generating documents: {e}")
            return []











