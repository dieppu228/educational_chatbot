"""Fallback handler for off-topic and chitchat queries"""

import logging
from typing import Optional
from .base_handler import BaseHandler
from LLM.prompts import FALLBACK_PROMPT
from config import settings


class FallbackHandler(BaseHandler):
    """Handle off-topic or chitchat queries gracefully."""
    
    def handle(self, query: str) -> str:
        """
        Generate response for off-topic query.
        
        Args:
            query: User query that doesn't fit main workflow
        
        Returns:
            str: Friendly response guiding user back to learning
        """
        self.logger.info(f"Fallback handler: {query[:100]}...")
        
        try:
            prompt = FALLBACK_PROMPT.format(query=query)
            
            response = self._call_api(
                prompt,
                temperature=0.7,
                response_mime='text/plain'
            )
            
            self.logger.debug("Fallback response generated")
            return response
        
        except Exception as e:
            self.logger.error(f"Fallback handling failed: {e}")
            # Return default friendly response
            return (
                "Xin chào! Tôi là trợ lý hỗ trợ học tập. "
                "Bạn muốn làm bài trắc nghiệm về khối nào? (10, 11, hay 12) "
                "Hoặc tôi có thể giúp bạn với những câu hỏi khác!"
            )


__all__ = ["FallbackHandler"]
