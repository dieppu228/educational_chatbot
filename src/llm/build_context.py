# Build context for LLM from retrieved results
import json
from typing import List, Dict


def build_context(query, retriever, top_k: int = 10) -> List[Dict]:
    """
    Build context for LLM from hybrid retrieval results.
    
    Args:
        query: User query string
        retriever: Hybrid retriever instance
        top_k: Number of top results to return
    
    Returns:
        List of context objects with metadata
    """
    results = retriever.hybrid_search_RRF(query, top_k=top_k, k=50)
    contexts = []
    
    for r in results:
        current_context = r.get('context', '')  # text context around the chunk
        content = r.get('content', '')           # main content of section
        metadata = r.get('metadata', {})         # metadata about section

        # Build context object
        context_obj = {
            'rrf_score': r.get('rrf_score'),
            'context': current_context,
            'content': content,
            'metadata': {
                'level': metadata.get('level', None),
                'title': metadata.get('title', ''),
                'type': metadata.get('type',''),
            }
        }

        contexts.append(context_obj)
    
    return contexts

