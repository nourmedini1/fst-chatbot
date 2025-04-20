import logging
from typing import List, Dict, Set
from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS
from local_storage_manager import LocalStorageManager
from config import Config
import os
import uuid

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class VectorStoreManager:
    def __init__(self, embedding_model):
        self.logger = logging.getLogger(__name__)
        self.embedding_model = embedding_model
        self.logger.debug(f"Initializing VectorStoreManager with model: {embedding_model.__class__.__name__}")
        
        try:
            if os.path.exists(Config.VECTOR_STORE_PATH):
                self.logger.debug(f"Found existing vector store at {Config.VECTOR_STORE_PATH}")
                self.vector_store = FAISS.load_local(
                    Config.VECTOR_STORE_PATH, 
                    self.embedding_model
                )
                store_size = len(self.vector_store.index_to_docstore_id)
                self.logger.debug(f"Loaded vector store contains {store_size} documents")
            else:
                self.logger.debug(f"Creating new vector store at {Config.VECTOR_STORE_PATH}")
                self.vector_store = FAISS.from_texts(
                    texts=["initialization_placeholder"], 
                    embedding=self.embedding_model
                )
                self.logger.debug("Testing vector store initialization...")
                test_result = self.vector_store.similarity_search("test", k=1)
                self.logger.debug(f"Test search returned {len(test_result)} results")
            
            # Verify vector store attributes
            self.logger.debug(f"Vector store attributes:")
            self.logger.debug(f"- Index type: {type(self.vector_store.index)}")
            self.logger.debug(f"- Docstore size: {len(self.vector_store.docstore._dict)}")
            self.logger.debug(f"- Index to docstore mapping size: {len(self.vector_store.index_to_docstore_id)}")
            
            # Initialize local storage manager
            self.local_storage_manager = LocalStorageManager()
            
        except Exception as e:
            self.logger.error(f"Failed to initialize vector store: {e}", exc_info=True)
            raise

    def add_documents(self, documents: List[Document], filename: str) -> bool:
        """Add documents to the vector store."""
        try:
            if not documents:
                self.logger.warning("No documents provided to add.")
                return False
            
            self.logger.debug(f"Adding {len(documents)} documents from {filename}")
            
            # Debug document contents
            for i, doc in enumerate(documents[:2]):
                self.logger.debug(f"Document {i} preview:")
                self.logger.debug(f"- Content length: {len(doc.page_content)}")
                self.logger.debug(f"- Metadata: {doc.metadata}")
                
            # Ensure each document has a document_id
            doc_ids = []
            for doc in documents:
                if 'document_id' not in doc.metadata:
                    doc.metadata['document_id'] = str(uuid.uuid4())
                doc_ids.append(doc.metadata['document_id'])
                
            # Store initial size
            initial_size = len(self.vector_store.index_to_docstore_id)
            self.logger.debug(f"Vector store size before addition: {initial_size}")
            
            # Add documents to vector store
            self.vector_store.add_documents(documents)
            
            # Verify addition
            final_size = len(self.vector_store.index_to_docstore_id)
            self.logger.debug(f"Vector store size after addition: {final_size}")
            self.logger.debug(f"Added {final_size - initial_size} new documents")
            
            # Store document mapping
            self.local_storage_manager.store_document_ids(filename, doc_ids)
            
            # Save vector store to disk
            self.persist_vector_store()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding documents: {e}", exc_info=True)
            return False

    def search_documents(self, query: str, k: int = 5) -> List[Document]:
        """Search for relevant documents."""
        try:
            self.logger.debug(f"Searching for query: {query}, k={k}")
            results = self.vector_store.similarity_search(query, k=k)
            self.logger.debug(f"Found {len(results)} matching documents")
            return results
        except Exception as e:
            self.logger.error(f"Error searching documents: {e}", exc_info=True)
            return []

    def delete_documents(self, filename: str) -> bool:
        """Delete documents associated with a filename."""
        try:
            doc_ids = self.local_storage_manager.get_document_ids_by_filename(filename)
            if not doc_ids:
                self.logger.warning(f"No documents found for filename: {filename}")
                return False
                
            self.logger.debug(f"Deleting {len(doc_ids)} documents for {filename}")
            self.vector_store.delete(doc_ids)
            self.local_storage_manager.remove_document_mapping(filename)
            
            # Verify deletion
            remaining_docs = len(self.vector_store.index_to_docstore_id)
            self.logger.debug(f"Vector store now contains {remaining_docs} documents")
            
            self.persist_vector_store()
            return True
            
        except Exception as e:
            self.logger.error(f"Error deleting documents: {e}", exc_info=True)
            return False

    def persist_vector_store(self) -> None:
        """Save vector store to disk."""
        try:
            self.vector_store.save_local(Config.VECTOR_STORE_PATH)
            self.logger.debug(f"Vector store saved to {Config.VECTOR_STORE_PATH}")
        except Exception as e:
            self.logger.error(f"Error saving vector store: {e}", exc_info=True)

    def get_store_size(self) -> int:
        """Get the number of documents in the store."""
        return len(self.vector_store.index_to_docstore_id)