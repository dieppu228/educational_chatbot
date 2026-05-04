import re
from typing import Set, Optional, List


class ContextAnalyzer:
    
    # Pronouns that might reference previous context
    PRONOUNS = {
        "nó", "nó", "cái này", "cái đó", "cái kia",
        "điều này", "điều đó", "điều kia",
        "bài này", "bài đó", "bài kia",
        "nó", "chúng nó", "chúng", "tôi", "bạn", "anh", "chị",
    }
    
    # Words indicating comparison
    COMPARATIVE = {
        "so sánh", "khác nhau", "so với", "tương tự",
        "giống như", "khác", "giống", "hơn", "kém",
        "đặc biệt hơn", "khác biệt",
    }
    
    # Words that often start ellipsis (incomplete sentences)
    ELLIPSIS_STARTS = {
        "và", "nhưng", "hoặc", "thế", "vậy",
        "thế nên", "vì vậy", "do đó", "vì thế",
        "tuy vậy", "tuy nhiên", "hơn nữa",
    }
    
    # Modal verbs that suggest dependency on context
    MODALS = {
        "nên", "có thể", "phải", "cần", "được",
        "hãy", "vui lòng", "làm ơn",
    }
    
    def __init__(self):
        pass
    
    def needs_contextualization(self, query: str, history: str) -> bool:
        # No history = no context needed
        if not history or not history.strip():
            return False
        
        query_lower = query.lower().strip()
        
        # Empty query shouldn't need context
        if not query_lower:
            return False
        
        # Check for pronouns referencing previous context
        if self._has_pronouns(query_lower):
            return True
        
        # Check for comparative words
        if self._has_comparative(query_lower):
            return True
        
        # Check if query starts with ellipsis marker
        if self._starts_with_ellipsis(query_lower):
            return True
        
        # Check for modal verbs suggesting implicit context
        if self._has_modals(query_lower):
            return True
        
        # Very short queries often depend on context
        if len(query_lower.split()) <= 3:
            # Check if it's a meaningful short query (not just "ok", "yes", etc)
            if self._is_affirmation_only(query_lower):
                return True
        
        return False
    
    def _has_pronouns(self, query: str) -> bool:
        words = query.split()
        for pronoun in self.PRONOUNS:
            if pronoun in words or pronoun in query:
                return True
        return False
    
    def _has_comparative(self, query: str) -> bool:
        for comp in self.COMPARATIVE:
            if comp in query:
                return True
        return False
    
    def _starts_with_ellipsis(self, query: str) -> bool:
        words = query.split()
        if words:
            first_word = words[0].lower().strip(".,!?;:")
            return first_word in self.ELLIPSIS_STARTS
        return False
    
    def _has_modals(self, query: str) -> bool:
        for modal in self.MODALS:
            if modal in query:
                return True
        return False
    
    def _is_affirmation_only(self, query: str) -> bool:
        affirmations = {"ok", "okay", "oke", "yes", "được", "vâng", "ừ", "a", "ai"}
        return query.lower().strip() in affirmations
    
    def extract_context_from_history(
        self,
        query: str,
        history: str,
        max_context_length: int = 1000
    ) -> str:
        if not history or not history.strip():
            return ""
        
        lines = history.strip().split('\n')
        N = len(lines)
        
        # 1. Prepare query keywords (filter out very short words/stop words)
        q_keywords = set(re.findall(r'\w{2,}', query.lower()))
        if not q_keywords:
            # Fallback to simple sliding window if no keywords
            return self._fallback_recency_only(lines, max_context_length)
            
        scored_lines = []
        for i, line in enumerate(lines):
            # Strip speaker prefix to score content only
            content = re.sub(r'^(user|assistant):\s*', '', line, flags=re.I).lower()
            line_keywords = set(re.findall(r'\w{2,}', content))
            
            # Keyword score: overlap percentage
            kw_score = len(q_keywords & line_keywords) / len(q_keywords)
            
            # Recency score: more recent = higher score (0 to 1.0)
            recency_score = (i + 1) / N
            
            # Hybrid total (Keyword weighted heavily)
            total_score = (kw_score * 0.7) + (recency_score * 0.3)
            
            scored_lines.append({
                "score": total_score,
                "text": line,
                "idx": i
            })
            
        # 2. Select top lines until limit reached
        scored_lines.sort(key=lambda x: x["score"], reverse=True)
        
        selected = []
        current_len = 0
        for item in scored_lines:
            if current_len + len(item["text"]) > max_context_length:
                break
            selected.append(item)
            current_len += len(item["text"])
            
        # 3. Sort back to original order for conversation flow
        selected.sort(key=lambda x: x["idx"])
        
        return '\n'.join([item["text"] for item in selected])

    def _fallback_recency_only(self, lines: List[str], max_len: int) -> str:
        context_lines = []
        total_length = 0
        for line in reversed(lines):
            if total_length + len(line) > max_len:
                break
            context_lines.append(line)
            total_length += len(line)
        return '\n'.join(reversed(context_lines))


__all__ = ["ContextAnalyzer"]
