from pdf_processor.geminiapicontroller import GeminiAPIController


class PDFAnalyzer:
    def __init__(self):
        print("Initialized PDF Analyzer")

    def analyze_pdf(self):
        gemini_controller = GeminiAPIController("myKey")
        gemini_controller.load_api_key()
        pass