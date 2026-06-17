from fastapi import APIRouter

from app.models.schemas import ChatRequest

from app.models.schemas import ChatResponse

from app.services.llm_service import llm


router = APIRouter(
    prefix="/api",
    tags=["Chat"]
)


@router.post(
    "/chat",
    response_model=ChatResponse
)
async def chat(request: ChatRequest):

    answer = llm.generate_response(
        request.message
    )

    return ChatResponse(
        response=answer
    )
