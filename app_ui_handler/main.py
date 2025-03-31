import time

import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from pdf_processor.geminiapicontroller import GeminiAPIController
from pdf_processor.main import PDFAnalyzer


class PDF2XLApp:
    def __init__(self):
        """
        Initializes the app and sets up the basic page layout
        """

        self._api_key = GeminiAPIController.load_api_key()

        st.set_page_config(page_title="PDF2XL", layout="wide")
        st.markdown("# :red[PDF] :gray[2] XL")
        st.markdown("#### :gray[By Ashwin]")
        st.divider()

    def setup_sidebar(self):
        with st.sidebar:
            st.markdown("## How to get API Key?")
            st.markdown("""
            1. Open Google AI Studio
            2. Click 'Get API Key'
            3. Click 'Generate API Key'
            4. Copy the key here]
            
            All Done!""")

            st.divider()

            self.api_key_input = st.text_input(label="Enter API Key", value=self._api_key or "", type="password")
            if st.button("Save API Key"):
                self.save_api_key(self.api_key_input)
                st.success("API Key saved!")


    def save_api_key(self, new_key: str):
        GeminiAPIController.update_api_key(new_key)

    def locateFileReceiver(self) -> UploadedFile:
        st.subheader("Upload the file")
        return st.file_uploader( label="Upload all PDFs", label_visibility="collapsed", type="pdf", accept_multiple_files=True)

    def renderFileAnalysis(self):
        st.divider()
        with st.spinner(text="Processing your file using your computer..."):
            pdf_processor = PDFAnalyzer()
            pdf_processor.analyze_pdf()
            time.sleep(10)
            st.write("Done")