
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from src.config.config import settings
from src.config.genai_client import create_genai_client
from src.llm.prompts import SYSTEM_PROMPT_SHORT


class BaseHandler(ABC):
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = settings.LLM_MODEL
    ):
        self.api_key = api_key or settings.GENAI_API_KEY
        self.model = model
        
        if not self.api_key:
            raise ValueError("GENAI_API_KEY not set in environment or config")
        
        # Initialize Google Generative AI client
        try:
            self.client = create_genai_client(api_key=self.api_key)
        except ImportError:
            raise ImportError("google-generativeai not installed")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize API client: {e}")
    
    @abstractmethod
    def handle(self, **kwargs) -> str:
        pass
    
    async def handle_async(self, **kwargs) -> str:
        return self.handle(**kwargs)
    
    def _call_api(
        self,
        prompt: str,
        temperature: float = 0.0,
        response_mime: str = "text/plain",
        include_system_prompt: bool = True,
        **kwargs
    ) -> str:
        try:
            # Prepend system prompt for consistent bot identity
            full_prompt = prompt
            if include_system_prompt:
                full_prompt = f"{SYSTEM_PROMPT_SHORT}\n\n{prompt}"

            config = {
                'temperature': temperature,
                'response_mime_type': response_mime,
                'top_p': kwargs.get('top_p', 0.95),
            }
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=full_prompt,
                config=config
            )
            
            return response.text
        
        except Exception as e:
            self._handle_error(e)
    
    async def _call_api_async(
        self,
        prompt: str,
        temperature: float = 0.0,
        response_mime: str = "text/plain",
        include_system_prompt: bool = True,
        **kwargs
    ) -> str:
        try:
            # Prepend system prompt for consistent bot identity
            full_prompt = prompt
            if include_system_prompt:
                full_prompt = f"{SYSTEM_PROMPT_SHORT}\n\n{prompt}"

            config = {
                'temperature': temperature,
                'response_mime_type': response_mime,
                'top_p': kwargs.get('top_p', 0.95),
            }
            
            response = await self.client.aio.models.generate_content(
                model=self.model,
                contents=full_prompt,
                config=config
            )
            
            return response.text
        
        except Exception as e:
            self._handle_error(e)
    
    def _handle_error(self, error: Exception) -> None:
        error_msg = f"Error in {self.__class__.__name__}: {str(error)}"
        raise RuntimeError(error_msg) from error
    
    def _validate_json_response(self, response: str) -> bool:
        try:
            import json
            json.loads(response)
            return True
        except json.JSONDecodeError:
            return False


__all__ = ["BaseHandler"]
