from groq import Groq

from app.config.settings import settings


class LLMService:

    def __init__(self):

        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

    def generate_response(self, message: str):

        response = self.client.chat.completions.create(

            model=settings.MODEL_NAME,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are CloudOps AI Copilot."
                        "Help engineers understand cloud technologies,"
                        "Kubernetes, AWS, Azure, Docker and Terraform."
                    ),
                },
                {
                    "role": "user",
                    "content": message,
                },
            ],

            temperature=0.2,

            max_tokens=1024,
        )

        return response.choices[0].message.content


llm = LLMService()
