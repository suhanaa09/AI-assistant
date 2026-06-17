from dotenv import load_dotenv
import os

load_dotenv()


class Settings:

    def __init__(self):

        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")

        self.MODEL_NAME = os.getenv("MODEL_NAME")

        if self.GROQ_API_KEY is None:

            raise Exception("Groq API Key Missing")


settings = Settings()
