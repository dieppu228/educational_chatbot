from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class PromptTemplate:
    name: str
    template: str
    required_vars: List[str] = field(default_factory=list)
    optional_vars: List[str] = field(default_factory=list)
    version: str = "1.0"
    description: str = ""

    def __post_init__(self):
        self._validate_template()

    def _validate_template(self) -> None:
        found_vars = set(re.findall(r"\{(\w+)\}", self.template))
        for var in self.required_vars:
            if var not in found_vars:
                raise ValueError(f"Required variable '{var}' not found in template '{self.name}'")

    def format(self, **kwargs) -> str:
        missing = [var for var in self.required_vars if var not in kwargs]
        if missing:
            raise ValueError(f"Missing required variables for '{self.name}': {missing}")
        try:
            return self.template.format(**kwargs)
        except KeyError as exc:
            raise ValueError(f"Variable {exc} not found in template") from exc

    def __str__(self) -> str:
        return f"PromptTemplate(name='{self.name}', version='{self.version}')"

    def __repr__(self) -> str:
        return f"PromptTemplate(name='{self.name}', required_vars={self.required_vars}, version='{self.version}')"


def create_prompt(name, template, required_vars, optional_vars=None, version="1.0", description=""):
    return PromptTemplate(
        name=name,
        template=template,
        required_vars=required_vars,
        optional_vars=optional_vars or [],
        version=version,
        description=description,
    )


class PromptManager:
    def __init__(self, prompt_dir: Optional[Path] = None):
        self.prompt_dir = prompt_dir or Path(__file__).with_name("md")
        self._cache: Dict[str, str] = {}

    def load(self, name: str, *, reload: bool = False) -> str:
        key = self._normalize_name(name)
        if not reload and key in self._cache:
            return self._cache[key]

        path = self.prompt_dir / f"{key}.md"
        if not path.exists():
            raise KeyError(f"Prompt file not found: {path}")

        text = path.read_text(encoding="utf-8")
        self._cache[key] = text
        return text

    def format(self, name: str, **kwargs) -> str:
        return self.load(name).format(**kwargs)

    def list_prompts(self) -> List[str]:
        if not self.prompt_dir.exists():
            return []
        return sorted(path.stem for path in self.prompt_dir.glob("*.md"))

    def clear_cache(self) -> None:
        self._cache.clear()

    @staticmethod
    def _normalize_name(name: str) -> str:
        return name[:-3] if name.endswith(".md") else name


__all__ = ["PromptManager", "PromptTemplate", "create_prompt"]
