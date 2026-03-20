"""Context analyzer for intelligent query contextualization"""

from typing import Set, Optional


class ContextAnalyzer:
    """Analyze if a query needs contextualization from conversation history."""
    
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
        """Initialize context analyzer."""
        pass
    
    def needs_contextualization(self, query: str, history: str) -> bool:
        """
        Determine if query needs contextualization from conversation history.
        
        Args:
            query: Current user query
            history: Conversation history (can be empty string)
        
        Returns:
            bool: True if query likely needs history context, False otherwise
        """
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
        """Check if query contains pronouns."""
        words = query.split()
        for pronoun in self.PRONOUNS:
            if pronoun in words or pronoun in query:
                return True
        return False
    
    def _has_comparative(self, query: str) -> bool:
        """Check if query contains comparative words."""
        for comp in self.COMPARATIVE:
            if comp in query:
                return True
        return False
    
    def _starts_with_ellipsis(self, query: str) -> bool:
        """Check if query starts with ellipsis marker."""
        words = query.split()
        if words:
            first_word = words[0].lower().strip(".,!?;:")
            return first_word in self.ELLIPSIS_STARTS
        return False
    
    def _has_modals(self, query: str) -> bool:
        """Check if query contains modal verbs."""
        for modal in self.MODALS:
            if modal in query:
                return True
        return False
    
    def _is_affirmation_only(self, query: str) -> bool:
        """
        Check if query is just an affirmation without content.
        
        Examples: "yes", "ok", "oke", "được", "vâng"
        """
        affirmations = {"ok", "okay", "oke", "yes", "được", "vâng", "ừ", "a", "ai"}
        return query.lower().strip() in affirmations
    
    def extract_context_from_history(
        self,
        history: str,
        max_context_length: int = 1000
    ) -> str:
        """
        Extract relevant context from conversation history.
        
        Args:
            history: Full conversation history
            max_context_length: Maximum length of extracted context
        
        Returns:
            str: Relevant context snippet
        """
        if not history:
            return ""
        
        # Take last N characters from history (most recent context)
        lines = history.strip().split('\n')
        
        context_lines = []
        total_length = 0
        
        for line in reversed(lines):
            if total_length + len(line) > max_context_length:
                break
            context_lines.append(line)
            total_length += len(line)
        
        return '\n'.join(reversed(context_lines))


__all__ = ["ContextAnalyzer"]
