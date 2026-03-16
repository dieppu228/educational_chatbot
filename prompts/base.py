"""
Base PromptTemplate class for managing prompt templates.
Provides validation, formatting, and versioning for prompts.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import re


@dataclass
class PromptTemplate:
    """
    Base class for managing LLM prompt templates.
    
    Features:
    - Variable validation before formatting
    - Version tracking for prompt iterations
    - Metadata for prompt documentation
    
    Usage:
        template = PromptTemplate(
            name="question_generation",
            template="Generate {num_questions} questions about {topic}",
            required_vars=["num_questions", "topic"],
            version="1.0"
        )
        
        prompt = template.format(num_questions=3, topic="encryption")
    """
    
    name: str
    template: str
    required_vars: List[str] = field(default_factory=list)
    optional_vars: List[str] = field(default_factory=list)
    version: str = "1.0"
    description: str = ""
    
    def __post_init__(self):
        """Validate template on creation"""
        self._validate_template()
    
    def _validate_template(self) -> None:
        """Ensure all required_vars are present in template"""
        # Find all {var} patterns in template
        found_vars = set(re.findall(r'\{(\w+)\}', self.template))
        
        # Check required vars are in template
        for var in self.required_vars:
            if var not in found_vars:
                raise ValueError(
                    f"Required variable '{var}' not found in template '{self.name}'"
                )
    
    def format(self, **kwargs) -> str:
        """
        Format template with provided variables.
        
        Args:
            **kwargs: Variable values to substitute
            
        Returns:
            Formatted prompt string
            
        Raises:
            ValueError: If required variable is missing
        """
        # Check all required vars are provided
        missing = [var for var in self.required_vars if var not in kwargs]
        if missing:
            raise ValueError(
                f"Missing required variables for '{self.name}': {missing}"
            )
        
        # Format template
        try:
            return self.template.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Variable {e} not found in template")
    
    def get_variables(self) -> Dict[str, List[str]]:
        """Get all variables (required and optional)"""
        return {
            "required": self.required_vars,
            "optional": self.optional_vars,
        }
    
    def __str__(self) -> str:
        return f"PromptTemplate(name='{self.name}', version='{self.version}')"
    
    def __repr__(self) -> str:
        return (
            f"PromptTemplate(name='{self.name}', "
            f"required_vars={self.required_vars}, "
            f"version='{self.version}')"
        )


def create_prompt(
    name: str,
    template: str,
    required_vars: List[str],
    optional_vars: Optional[List[str]] = None,
    version: str = "1.0",
    description: str = ""
) -> PromptTemplate:
    """
    Factory function to create PromptTemplate instances.
    
    Args:
        name: Unique identifier for the prompt
        template: The prompt template string with {variables}
        required_vars: List of required variable names
        optional_vars: List of optional variable names
        version: Version string for tracking changes
        description: Human-readable description
        
    Returns:
        PromptTemplate instance
    """
    return PromptTemplate(
        name=name,
        template=template,
        required_vars=required_vars,
        optional_vars=optional_vars or [],
        version=version,
        description=description
    )


__all__ = ["PromptTemplate", "create_prompt"]
