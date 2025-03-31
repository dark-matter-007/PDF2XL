import google.generativeai as genai
from PIL import Image
from pdf2image import convert_from_path, convert_from_bytes
from streamlit.runtime.uploaded_file_manager import UploadedFile
import io
import base64

class GeminiAPIController:
    def __init__(self, api_key: str = None):
        if api_key is not None:
            self.api_key = api_key
        else:
            self.api_key = self.load_api_key()  # Load API key

        if self.api_key == "API Key Error":
            raise ValueError("API Key not found. Please set it using GeminiAPIController.update_api_key()")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')  # Use the vision model

        print("Initialized Gemma API Controller")

    @staticmethod
    def update_api_key(new_key):
        config_path = "./resources/config.toml"
        try:
            import toml
            with open(config_path, "w") as file:
                new_config = {"API_KEY": new_key}
                toml.dump(new_config, file)
        except Exception as e:
            print(f"Error writing new config: {e}")
            raise

    @staticmethod
    def load_api_key() -> str:
        config_path = "./resources/config.toml"
        try:
            import toml
            with open(config_path, "r") as file:
                config = toml.load(file)
                api_key = config.get("API_KEY")
                if api_key is None:
                    raise ValueError("API_KEY not found in config.toml")
                return api_key
        except FileNotFoundError:
            print(f"Error: config.toml not found at {config_path}")
            return "API Key Error"
        except toml.TomlDecodeError:
            print(f"Error: Invalid TOML format in {config_path}")
            return "API Key Error"
        except Exception as e:
            print(f"Error loading API Key: {e}")
            return "API Key Error"

    def get_xl_for_images(self, images: list[Image or str or UploadedFile]):
        """
        Extracts data from images (or PDFs) and returns it in a structured format.

        Args:
            images: A list of PIL Images, image file paths (str), or Streamlit UploadedFile objects.
                    If a string path is provided and ends with '.pdf', the file is treated as a PDF.

        Returns:
            str: A string representation of the extracted data, formatted as a CSV.
                 Returns None on error.
        """
        if not images:
            print("Error: No images provided.")
            return None

        prompt = "Extract the data from this image and return it as a CSV.  Include the header row. Do not include any explanations or introductory text.  Just the CSV data."

        contents = []
        for image in images:
            image_data = None
            mime_type = None
            if isinstance(image, Image.Image):
                # PIL Image
                buffered = io.BytesIO()
                image.save(buffered, format="JPEG")  # Or PNG, choose best for your needs
                image_data = buffered.getvalue()
                mime_type = "image/jpeg"
            elif isinstance(image, str):
                if image.lower().endswith(".pdf"):
                    try:
                        pdf_images = convert_from_path(image)  # Use convert_from_path for file path
                        for pdf_image in pdf_images:  # Iterate through pages of the PDF
                            buffered = io.BytesIO()
                            pdf_image.save(buffered, format="JPEG")
                            image_data = buffered.getvalue()
                            mime_type = "image/jpeg"
                            contents.append(
                                {
                                    "mime_type": mime_type,
                                    "data": base64.b64encode(image_data).decode(),
                                }
                            )
                        continue  # Important: Processed all pages, go to next image in list
                    except Exception as e:
                        print(f"Error processing PDF {image}: {e}")
                        return None
                else:
                    # Assume it's a file path to an image
                    try:
                        with open(image, 'rb') as image_file:
                            image_data = image_file.read()
                        mime_type = "image/jpeg"  # or image/png, you may need to adjust
                    except Exception as e:
                        print(f"Error reading image file {image}: {e}")
                        return None

            elif isinstance(image, UploadedFile):
                # Streamlit UploadedFile
                try:
                    image_data = image.read()
                    mime_type = image.type
                    if image.name.lower().endswith(".pdf"):
                        pdf_images = convert_from_bytes(image_data)
                        for pdf_image in pdf_images:
                            buffered = io.BytesIO()
                            pdf_image.save(buffered, format="JPEG")
                            image_data = buffered.getvalue()
                            mime_type = "image/jpeg"
                            contents.append(
                                {
                                    "mime_type": mime_type,
                                    "data": base64.b64encode(image_data).decode(),
                                }
                            )
                        continue
                except Exception as e:
                    print(f"Error processing UploadedFile {image.name}: {e}")
                    return None
            else:
                print(f"Error: Unsupported image type: {type(image)}")
                return None
            if image_data:
                contents.append(
                    {
                        "mime_type": mime_type,
                        "data": base64.b64encode(image_data).decode(),
                    }
                )

        response = self.model.generate_content(
            [prompt] + contents,  # Pass prompt and images
            generation_config=genai.GenerationConfig(max_output_tokens=2048),
        )

        if response.text:
            return response.text
        else:
            return "No data extracted."
