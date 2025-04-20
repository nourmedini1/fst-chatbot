import sqlite3
import json
import logging
from typing import List


class LocalStorageManager:
    """
    Manages local storage for document mappings using SQLite.
    Maps filenames to document IDs for efficient retrieval and deletion.
    """
    
    def __init__(self, db_path: str = "document_index.db"):
        """
        Initialize the local storage manager.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self._initialize_db()
    
    def _initialize_db(self):
        """Initialize the SQLite database for document mapping."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS document_mapping (
                    filename TEXT PRIMARY KEY,
                    document_ids TEXT
                )
                ''')
                conn.commit()
            self.logger.info(f"Initialized document mapping database at {self.db_path}")
        except Exception as e:
            self.logger.error(f"Failed to initialize database: {e}")
            raise
    
    def store_document_ids(self, filename: str, doc_ids: List[str]):
        """
        Store document IDs for a filename in the SQLite database.
        
        Args:
            filename: The filename associated with the document IDs
            doc_ids: List of document IDs to store
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT document_ids FROM document_mapping WHERE filename = ?", (filename,))
                result = cursor.fetchone()
                
                if result:
                    existing_ids = json.loads(result[0])
                    updated_ids = list(set(existing_ids + doc_ids))  
                    cursor.execute(
                        "UPDATE document_mapping SET document_ids = ? WHERE filename = ?", 
                        (json.dumps(updated_ids), filename)
                    )
                else:
                    cursor.execute(
                        "INSERT INTO document_mapping (filename, document_ids) VALUES (?, ?)",
                        (filename, json.dumps(doc_ids))
                    )
                conn.commit()
                self.logger.debug(f"Stored {len(doc_ids)} document IDs for filename '{filename}'")
        except Exception as e:
            self.logger.error(f"Error storing document IDs: {e}")
            raise
    
    def get_document_ids_by_filename(self, filename: str) -> List[str]:
        """
        Get document IDs for a filename from the SQLite database.
        
        Args:
            filename: The filename to query
            
        Returns:
            List of document IDs associated with the filename
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT document_ids FROM document_mapping WHERE filename = ?", (filename,))
                result = cursor.fetchone()
                if result:
                    return json.loads(result[0])
                return []
        except Exception as e:
            self.logger.error(f"Error retrieving document IDs: {e}")
            return []
    
    def remove_document_mapping(self, filename: str) -> bool:
        """
        Remove document mapping for a filename from the database.
        
        Args:
            filename: The filename to remove
            
        Returns:
            bool: True if mapping was removed, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM document_mapping WHERE filename = ?", (filename,))
                conn.commit()
                if cursor.rowcount > 0:
                    self.logger.debug(f"Removed document mapping for filename '{filename}'")
                    return True
                return False
        except Exception as e:
            self.logger.error(f"Error removing document mapping: {e}")
            return False
    
    def get_all_filenames(self) -> List[str]:
        """
        Get all filenames stored in the database.
        
        Returns:
            List of filenames
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT filename FROM document_mapping")
                results = cursor.fetchall()
                return [row[0] for row in results]
        except Exception as e:
            self.logger.error(f"Error retrieving filenames: {e}")
            return []
    
    def clear_all_mappings(self):
        """Clear all document mappings from the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM document_mapping")
                conn.commit()
                self.logger.info("Cleared all document mappings")
        except Exception as e:
            self.logger.error(f"Error clearing document mappings: {e}")
            raise