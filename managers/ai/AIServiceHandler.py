from abstractions.enumerations.AiTypeEnum import AiTypeEnum

ai_service_map = {
    AiTypeEnum.OpenAI.value: AiTypeEnum.OpenAI,
}

class AIServiceHandler:
    @staticmethod
    def get_ai_service(ai_type: str):
        if ai_type not in ai_service_map:
            raise ValueError(f"Unsupported AI type: {ai_type}. Supported types are: {list(ai_service_map.keys())}")

        ai_type = ai_service_map[ai_type]

        if ai_type == AiTypeEnum.OpenAI.value:
            from managers.ai.OpenAIServiceManager import OpenAIServiceManager
            return OpenAIServiceManager
        else:
            raise NotImplementedError
