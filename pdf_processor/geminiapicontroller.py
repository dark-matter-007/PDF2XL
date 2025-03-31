import streamlit
import toml
import os
from streamlit.runtime.uploaded_file_manager import UploadedFile

class GeminiAPIController:
    def __init__(self, api_key: str = None):
        if api_key is not None:
            self.api_key = api_key

        print("Initialized Gemma API Controller")

    @staticmethod
    def update_api_key(new_key):
        config_path = "./resources/config.toml" # because the class is called from the root file
        try:
            with open(config_path, "w") as file:
                new_config = {"API_KEY": new_key}
                toml.dump(new_config, file)
        except:
            print("Error writing new config")

    @staticmethod
    def load_api_key() -> str:
        # config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.toml") #this is the fix.
        config_path = "./resources/config.toml" # because the class is called from the root file
        try:
            with open(config_path, "r") as file:
                api_key = toml.loads(file.read()).get("API_KEY")
                return api_key
        except FileNotFoundError:
            print(f"Error: config.toml not found at {config_path}")
            return "API Key Error"

    def analyzePDF(self, file: UploadedFile):
        pass