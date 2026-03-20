"""Question generation handler"""

from typing import List, Optional, Dict
import json
from .base_handler import BaseHandler
from src.llm.prompts import QUESTION_GENERATION_PROMPT
from src.llm.validators import validate_num_questions, validate_json_response
from src.llm.utils import extract_num_questions, calculate_adaptive_questions, format_contexts
from src.config import settings
from core import MCQResponse


class QuestionGenerator(BaseHandler):
    """Generate multiple-choice questions from query and retrieved documents."""
    
    def __init__(
        self,
        retriever,
        reranker,
        api_key: Optional[str] = None,
        model: str = settings.LLM_MODEL
    ):
        """
        Initialize QuestionGenerator.
        
        Args:
            retriever: Retriever instance for document search
            reranker: Reranker instance for document ranking
            api_key: Google Generative AI API key
            model: LLM model name
        """
        super().__init__(api_key, model)
        self.retriever = retriever
        self.reranker = reranker
    
    def handle(
        self,
        query: str,
        top_k: int = settings.RETRIEVER_TOP_K,
        rerank_top_n: int = settings.RERANKER_TOP_N
    ) -> str:
        """
        Generate multiple-choice questions from user query.
        
        Args:
            query: User query text
            top_k: Number of documents to retrieve
            rerank_top_n: Number of documents to use after reranking
        
        Returns:
            str: JSON string with MCQ format
        
        Raises:
            ValueError: If no contexts retrieved or invalid parameters
            RuntimeError: If API call fails
        """
        try:
            # Step 1: Retrieve and rerank documents
            contexts = self._get_contexts(query, top_k, rerank_top_n)
            
            if not contexts:
                raise ValueError("No relevant documents retrieved")
            
            # Step 2: Determine number of questions
            num_questions = self._determine_num_questions(query, len(contexts))
            
            # Step 3: Build prompt
            prompt = self._build_prompt(query, contexts, num_questions)
            
            # Step 4: Call LLM API
            response = self._call_api(
                prompt,
                temperature=settings.QUESTION_GENERATION_TEMPERATURE,
                response_mime='application/json'
            )
            
            # Step 5: Validate response
            if not validate_json_response(response):
                raise ValueError("API returned invalid JSON format")
            
            return response
        
        except Exception as e:
            self._handle_error(e)
    
    def _get_contexts(
        self,
        query: str,
        top_k: int,
        rerank_top_n: int
    ) -> List[Dict]:
        """
        Retrieve and rerank documents.
        
        Args:
            query: Search query
            top_k: Number of initial retrievals
            rerank_top_n: Number of final reranked results
        
        Returns:
            List of reranked document dictionaries
        """
        # BM25 + FAISS hybrid search with RRF
        results = self.retriever.hybrid_search_RRF(
            query,
            top_k=top_k,
            k=settings.RRF_K_WEIGHT
        )
        
        if not results:
            return []
        
        # Rerank results
        reranked = self.reranker.rerank(query, results, top_n=rerank_top_n)
        
        return reranked
    
    def _determine_num_questions(
        self,
        query: str,
        context_count: int
    ) -> int:
        """
        Determine number of questions to generate.
        
        Args:
            query: User query (may contain explicit question count)
            context_count: Number of retrieved contexts
        
        Returns:
            int: Number of questions to generate (1-10)
        """
        # Try to extract explicit number from query
        num = extract_num_questions(query)
        
        if num is None:
            # Use adaptive calculation based on context count
            num = calculate_adaptive_questions(context_count)
        
        return validate_num_questions(num)
    
    def _build_prompt(
        self,
        query: str,
        contexts: List[Dict],
        num_questions: int
    ) -> str:
        """
        Build the question generation prompt.
        
        Args:
            query: User query
            contexts: Retrieved context documents
            num_questions: Number of questions to generate
        
        Returns:
            str: Formatted prompt
        """
        context_text = format_contexts(contexts)
        
        return QUESTION_GENERATION_PROMPT.format(
            query=query,
            context=context_text,
            num_questions=num_questions
        )


__all__ = ["QuestionGenerator"]
