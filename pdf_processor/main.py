from PIL.Image import Image
from pdf2image import convert_from_bytes
from streamlit.runtime.uploaded_file_manager import UploadedFile

from pdf_processor.geminiapicontroller import GeminiAPIController


class PDFAnalyzer:
    def __init__(self, api_key: str):
        self.api_key = api_key
        print("Initialized PDF Analyzer")

    @staticmethod
    def get_pdf_images(file: UploadedFile) -> list[Image] | None:
        """
        Analyzes a PDF file uploaded via Streamlit, converting it to a list of PIL Images.

        Args:
            file (UploadedFile): The uploaded PDF file.

        Returns:
            list[PIL.Image.Image] or None: A list of PIL Images if successful, None otherwise.
        """
        if file is not None:
            try:
                images = convert_from_bytes(file.getvalue())
                return images
            except Exception as e:
                print(f"Error converting PDF: {e}")
                return None
        else:
            return None

    def analyze_pdf(self, file: UploadedFile):
        gemini_controller = GeminiAPIController(self.api_key)
        images = self.get_pdf_images(file)
        gemini_controller.get_xl_for_images(images)
        pass