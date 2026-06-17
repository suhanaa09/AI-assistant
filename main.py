from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router


app = FastAPI(

    title="CloudOps AI Copilot",

    version="1.0.0",

    description="Enterprise AI Assistant for Cloud Engineers"

)


app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)


app.include_router(router)


@app.get("/")

def root():

    return {

        "status": "Running",

        "application": "CloudOps AI Copilot"

    }
