# This is going to be the Entry point
import streamlit

from app_ui_handler.main import PDF2XLApp

if __name__ == '__main__':
    app = PDF2XLApp()

    app.setup_sidebar()
    file: list = app.locateFileReceiver()

    if file:  # Check if the list is not empty
        app.renderFileAnalysis()
    else:
        streamlit.write("No files uploaded yet.")

