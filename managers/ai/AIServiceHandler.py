from abstractions.enumerations.AiTypeEnum import AiTypeEnum

ai_service_map = {
    AiTypeEnum.OpenAI.value: AiTypeEnum.OpenAI,
}

class AIServiceHandler:
    @staticmethod
    def get_ai_service(llm_config: dict):
        ai_type = llm_config.get("ai_type")
        if ai_type not in ai_service_map:
            raise ValueError(f"Unsupported AI type: {ai_type}. Supported types are: {list(ai_service_map.keys())}")

        ai_type = ai_service_map[ai_type]

        llm_manager = None
        if ai_type == AiTypeEnum.OpenAI:
            from managers.ai.OpenAIServiceManager import OpenAIServiceManager

            llm_manager = OpenAIServiceManager(llm_config)
            llm_manager.configure()
        else:
            raise NotImplementedError

        return llm_manager
