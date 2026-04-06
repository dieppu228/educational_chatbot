"""Base handler class for all LLM handlers"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from src.config.config import settings
from src.llm.prompts import SYSTEM_PROMPT_SHORT


class BaseHandler(ABC):
    """
    Abstract base class for all LLM handlers.
    
    Provides common functionality for API calls and error handling.
    Automatically prepends system prompt to all LLM calls.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = settings.LLM_MODEL
    ):
        """
        Initialize base handler.
        
        Args:
            api_key: Google Generative AI API key. If None, uses GENAI_API_KEY from env
            model: Model name to use for API calls
        """
        self.api_key = api_key or settings.GENAI_API_KEY
        self.model = model
        
        if not self.api_key:
            raise ValueError("GENAI_API_KEY not set in environment or config")
        
        # Initialize Google Generative AI client
        try:
            from google import genai
            self.client = genai.Client(api_key=self.api_key)
        except ImportError:
            raise ImportError("google-generativeai not installed")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize API client: {e}")
    
    @abstractmethod
    def handle(self, **kwargs) -> str:
        """
        Main handler method - must be implemented by subclasses.
        
        Returns:
            str: Handler response
        """
        pass
    
    def _call_api(
        self,
        prompt: str,
        temperature: float = 0.0,
        response_mime: str = "text/plain",
        include_system_prompt: bool = True,
        **kwargs
    ) -> str:
        """
        Generic API call wrapper with error handling.
        Automatically prepends system prompt unless disabled.
        
        Args:
            prompt: The prompt to send to LLM
            temperature: Temperature for response generation
            response_mime: Response MIME type (text/plain or application/json)
            include_system_prompt: Whether to prepend system prompt (default True)
            **kwargs: Additional config parameters
        
        Returns:
            str: API response text
        
        Raises:
            RuntimeError: If API call fails
        """
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
    
    def _handle_error(self, error: Exception) -> None:
        """
        Unified error handling.
        
        Args:
            error: The exception that occurred
        
        Raises:
            RuntimeError: Always raises with context
        """
        error_msg = f"Error in {self.__class__.__name__}: {str(error)}"
        raise RuntimeError(error_msg) from error
    
    def _validate_json_response(self, response: str) -> bool:
        """
        Validate JSON response format.
        
        Args:
            response: Response text to validate
        
        Returns:
            bool: True if valid JSON, False otherwise
        """
        try:
            import json
            json.loads(response)
            return True
        except json.JSONDecodeError:
            return False


__all__ = ["BaseHandler"]
