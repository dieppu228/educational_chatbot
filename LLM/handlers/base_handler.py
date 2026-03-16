"""Base handler class for all LLM handlers"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from config import settings


class BaseHandler(ABC):
    """
    Abstract base class for all LLM handlers.
    
    Provides common functionality for API calls and error handling.
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
        **kwargs
    ) -> str:
        """
        Generic API call wrapper with error handling.
        
        Args:
            prompt: The prompt to send to LLM
            temperature: Temperature for response generation
            response_mime: Response MIME type (text/plain or application/json)
            **kwargs: Additional config parameters
        
        Returns:
            str: API response text
        
        Raises:
            RuntimeError: If API call fails
        """
        try:
            config = {
                'temperature': temperature,
                'response_mime_type': response_mime,
                'top_p': kwargs.get('top_p', 0.95),
            }
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
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
