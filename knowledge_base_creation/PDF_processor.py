import pdfplumber
import os
import logging


class PDFProcessor:
    def __init__(self, PDFs_folder_path : str ):
        self.pdf_folder_path = PDFs_folder_path
        self.logger = logging.getLogger(__name__)


    def _extract_text_from_pdf(self, pdf_path : str) -> str:
        """
        Extracts text from a PDF file.
        :param pdf_path: Path to the PDF file.
        :return: Extracted text as a string.
        """
        text = ''
        try:
            if not os.path.exists(pdf_path):
                self.logger.error(f"PDF file not found: {pdf_path}")
                return text
                
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text
            return text
        except Exception as e:
            self.logger.error(f"Error extracting text from PDF {pdf_path}: {e}")
            return text
    

    def _extract_metadata_from_pdf(self, pdf_path : str) -> dict:
        """
        Extracts simplified metadata from a PDF file.
        :param pdf_path: Path to the PDF file.
        :return: Dictionary with filename and creation date (if available).
        """
        filename = os.path.basename(pdf_path)  
        result_metadata = {
            'filename': filename
        }
        try:
            if not os.path.exists(pdf_path):
                self.logger.error(f"PDF file not found: {pdf_path}")
                return result_metadata
                
            with pdfplumber.open(pdf_path) as pdf:
                pdf_metadata = pdf.metadata
                if pdf_metadata and 'CreationDate' in pdf_metadata:
                    result_metadata['creation_date'] = pdf_metadata['CreationDate']
            
            return result_metadata
        except Exception as e:
            self.logger.error(f"Error extracting metadata from PDF {pdf_path}: {e}")
            return result_metadata
    
    def process_pdf(self,pdf_path : str) -> dict:
        """
        Processes a PDF file to extract text and metadata.
        :param pdf_path: Path to the PDF file.
        :return: Dictionary with extracted text and metadata.
        """
        try:
            if not os.path.exists(pdf_path):
                self.logger.error(f"PDF file not found: {pdf_path}")
                return {'text': '', 'metadata': {'filename': os.path.basename(pdf_path)}}
                
            text = self._extract_text_from_pdf(pdf_path)
            metadata = self._extract_metadata_from_pdf(pdf_path)
            
            return {
                'text': text,
                'metadata': metadata
            }
        except Exception as e:
            self.logger.error(f"Error processing PDF {pdf_path}: {e}")
            return {'text': '', 'metadata': {'filename': os.path.basename(pdf_path)}}




