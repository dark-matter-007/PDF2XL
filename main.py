# This is going to be the Entry point
import streamlit
from streamlit.runtime.uploaded_file_manager import UploadedFile

from app_ui_handler.main import PDF2XLApp
from pdf_processor.main import PDFAnalyzer

if __name__ == '__main__':
    app = PDF2XLApp()

    app.setup_sidebar()
    file: UploadedFile = app.locate_file_receiver()

    if file:  # Check if the list is not empty
        app.analyze_file(file)
    else:
        streamlit.write("No files uploaded yet.")

