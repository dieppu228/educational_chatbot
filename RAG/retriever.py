"""Document retriever with hybrid search (BM25 + FAISS)"""

import logging
import faiss
import numpy as np
from nltk.tokenize import word_tokenize
from rank_bm25 import BM25Okapi
from typing import List, Dict, Tuple, Optional
from utils import setup_logger


class Retriever:
    """
    Hybrid document retriever combining BM25 keyword search and FAISS vector search.
    
    Uses Reciprocal Rank Fusion (RRF) to combine ranking signals from both methods.
    """
    
    def __init__(self, model, logger: Optional[logging.Logger] = None):
        """
        Initialize retriever.
        
        Args:
            model: Sentence transformer model for embeddings
            logger: Logger instance
        """
        self.model = model
        self.bm25 = None
        self.index = None
        self.data = None
        self.logger = logger or setup_logger(__name__)
        self.logger.debug("Retriever initialized")
    
    def set_data(self, data: List[Dict]) -> None:
        """
        Set chunk data for retrieval.
        
        Args:
            data: List of chunk dictionaries
        """
        if not data:
            raise ValueError("Data cannot be empty")
        
        self.data = data
        self.logger.debug(f"Data set with {len(data)} chunks")
    
    def build_bm25(self, corpus_texts: List[str]) -> BM25Okapi:
        """
        Build BM25 index from corpus texts.
        
        Args:
            corpus_texts: List of text documents
        
        Returns:
            BM25Okapi instance
        
        Raises:
            ValueError: If corpus_texts is empty
        """
        if not corpus_texts:
            raise ValueError("corpus_texts cannot be empty")
        
        try:
            tokenized_corpus = [word_tokenize(text.lower()) for text in corpus_texts]
            self.bm25 = BM25Okapi(tokenized_corpus)
            self.logger.info(f"Built BM25 index with {len(corpus_texts)} documents")
            return self.bm25
        except Exception as e:
            self.logger.error(f"Failed to build BM25: {e}")
            raise
    
    def bm25_search(
        self,
        query: str,
        top_k: int = 5
    ) -> Tuple[List[Tuple[int, int, float]], List[float]]:
        """
        Search using BM25 keyword matching.
        
        Args:
            query: Search query
            top_k: Number of top results to return
        
        Returns:
            Tuple of:
                - List of (rank, doc_index, score) tuples
                - List of scores for top_k results
        
        Raises:
            ValueError: If BM25 not built yet
        """
        if self.bm25 is None:
            raise ValueError("BM25 not initialized. Call build_bm25() first")
        
        try:
            tokenized_query = word_tokenize(query.lower())
            scores = self.bm25.get_scores(tokenized_query)
            
            ranked_indices = np.argsort(scores)[::-1][:top_k]
            ranked_results = [
                (rank, int(idx), float(scores[idx]))
                for rank, idx in enumerate(ranked_indices)
            ]
            
            self.logger.debug(f"BM25 search returned {len(ranked_results)} results")
            return ranked_results, [float(scores[i]) for i in ranked_indices]
        
        except Exception as e:
            self.logger.error(f"BM25 search failed: {e}")
            raise
    
    def build_faiss_index(
        self,
        embeddings: np.ndarray,
        metric: str = "IP"
    ) -> faiss.Index:
        """
        Build FAISS vector index.
        
        Args:
            embeddings: Document embeddings matrix (n_docs x embedding_dim)
            metric: Distance metric ("IP" for inner product or "L2" for Euclidean)
        
        Returns:
            FAISS index instance
        
        Raises:
            ValueError: If metric not supported
        """
        if metric not in ["IP", "L2"]:
            raise ValueError("metric must be 'IP' or 'L2'")
        
        try:
            dim = embeddings.shape[1]
            
            if metric == "IP":
                self.index = faiss.IndexFlatIP(dim)
            else:
                self.index = faiss.IndexFlatL2(dim)
            
            self.index.add(embeddings.astype(np.float32))
            self.logger.info(f"Built FAISS {metric} index with {embeddings.shape[0]} embeddings")
            return self.index
        
        except Exception as e:
            self.logger.error(f"Failed to build FAISS index: {e}")
            raise
    
    def faiss_search(
        self,
        query: str,
        top_k: int = 5
    ) -> Tuple[List[Tuple[int, int, float]], List[float]]:
        """
        Search using FAISS vector similarity.
        
        Args:
            query: Search query
            top_k: Number of top results to return
        
        Returns:
            Tuple of:
                - List of (rank, doc_index, score) tuples
                - List of scores for top_k results
        
        Raises:
            ValueError: If FAISS index not built yet
        """
        if self.index is None:
            raise ValueError("FAISS index not initialized. Call build_faiss_index() first")
        
        try:
            query_vec = self.model.encode(
                [query],
                normalize_embeddings=True
            ).astype(np.float32)
            
            scores, indices = self.index.search(query_vec, top_k)
            
            ranked_results = [
                (rank, int(idx), float(scores[0][rank]))
                for rank, idx in enumerate(indices[0])
            ]
            
            self.logger.debug(f"FAISS search returned {len(ranked_results)} results")
            return ranked_results, [float(s) for s in scores[0]]
        
        except Exception as e:
            self.logger.error(f"FAISS search failed: {e}")
            raise
    
    def hybrid_search_RRF(
        self,
        query: str,
        top_k: int = 5,
        k: int = 60,
        weight_bm25: float = 0.3,
        weight_faiss: float = 0.7
    ) -> List[Dict]:
        """
        Hybrid search using Reciprocal Rank Fusion (RRF).
        
        Combines BM25 and FAISS rankings using RRF formula:
            RRF(d) = sum(1 / (k + rank_i(d)))
        
        Args:
            query: Search query
            top_k: Number of top results to return
            k: RRF parameter (constant, typically 60)
            weight_bm25: Weight for BM25 component (0-1)
            weight_faiss: Weight for FAISS component (0-1)
        
        Returns:
            List of ranked documents with metadata and RRF scores
        
        Raises:
            ValueError: If data not set or indices not built
        """
        if self.data is None:
            raise ValueError("Data not set. Call set_data() first")
        
        try:
            self.logger.debug(f"Starting hybrid search for query: {query[:50]}...")
            
            # Get BM25 results
            bm25_ranked, _ = self.bm25_search(query, top_k=top_k * 2)
            self.logger.debug(f"BM25 returned {len(bm25_ranked)} results")
            
            # Get FAISS results
            faiss_ranked, _ = self.faiss_search(query, top_k=top_k * 2)
            self.logger.debug(f"FAISS returned {len(faiss_ranked)} results")
            
            # Combine using RRF
            rrf_scores: Dict[int, float] = {}
            
            # Add BM25 contributions
            for rank, idx, _ in bm25_ranked:
                rrf_scores[idx] = rrf_scores.get(idx, 0) + (1 / (k + rank + 1)) * weight_bm25
            
            # Add FAISS contributions
            for rank, idx, _ in faiss_ranked:
                rrf_scores[idx] = rrf_scores.get(idx, 0) + (1 / (k + rank + 1)) * weight_faiss
            
            # Sort by RRF score
            sorted_rrf = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
            
            # Build result list
            results_for_retrieval = []
            for idx, score in sorted_rrf[:top_k]:
                chunk = self.data[idx]
                results_for_retrieval.append({
                    "rrf_score": float(score),
                    "context": chunk.get("context"),
                    "content": chunk.get("content"),
                    "metadata": chunk.get("metadata", {})
                })
            
            self.logger.info(f"Hybrid search returned {len(results_for_retrieval)} results")
            return results_for_retrieval
        
        except Exception as e:
            self.logger.error(f"Hybrid search failed: {e}")
            raise


__all__ = ["Retriever"]
