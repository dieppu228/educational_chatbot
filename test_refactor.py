"""Integration test for refactored modules"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("=" * 60)
print("REFACTOR INTEGRATION TEST")
print("=" * 60)

# Test 1: Config module
print("\n[1/5] Testing config module...")
try:
    from config import settings
    from config.constants import (
        MIN_QUESTIONS, MAX_QUESTIONS, TEMP_DETERMINISTIC,
        STATUS_FOUND, DIFFICULTY_EASY, VALID_GRADES
    )
    print("✓ Config loaded successfully")
    print(f"  - LLM Model: {settings.LLM_MODEL}")
    print(f"  - Min Questions: {MIN_QUESTIONS}")
    print(f"  - Max Questions: {MAX_QUESTIONS}")
    print(f"  - Valid Grades: {VALID_GRADES}")
except Exception as e:
    print(f"✗ Config failed: {e}")
    sys.exit(1)

# Test 2: Core models
print("\n[2/5] Testing Pydantic models...")
try:
    from core import (
        MCQOption, MCQQuestion, MCQResponse, ChunkMetadata,
        Chunk, ScoringResult, Query, ConversationContext
    )
    
    # Create test objects
    option = MCQOption(A="Option A", B="Option B", C="Option C", D="Option D")
    question = MCQQuestion(
        index=1,
        question="Test question?",
        options=option,
        correct_answer="A",
        explanation="Because..."
    )
    response = MCQResponse(mcq=[question])
    
    print("✓ Pydantic models initialized successfully")
    print(f"  - Created MCQ with {len(response.mcq)} questions")
except Exception as e:
    print(f"✗ Pydantic models failed: {e}")
    sys.exit(1)

# Test 3: Logger utility
print("\n[3/5] Testing logger utility...")
try:
    from utils import setup_logger
    logger = setup_logger("test_logger")
    logger.info("Logger working properly")
    print("✓ Logger initialized successfully")
except Exception as e:
    print(f"✗ Logger failed: {e}")
    sys.exit(1)

# Test 4: LLM handlers and utilities
print("\n[4/5] Testing LLM handlers and utilities...")
try:
    from LLM.validators import validate_num_questions, validate_json_response
    from LLM.utils import extract_num_questions, calculate_adaptive_questions
    
    # Test validators
    assert validate_num_questions(5) == 5
    assert validate_num_questions(20) == 10  # Capped at MAX
    assert validate_num_questions(None) == 3  # Default
    print("✓ Validators working correctly")
    
    # Test utils
    num = extract_num_questions("cho 3 câu hỏi")
    assert num == 3
    print("✓ Utils extraction working correctly")
    
    # Test adaptive
    adaptive = calculate_adaptive_questions(20)
    assert 4 <= adaptive <= 5
    print("✓ Adaptive calculation working correctly")
    
    # Test JSON validation
    valid_json = '{"mcq": [{"index": 1, "question": "Q?", "options": {"A": "a", "B": "b", "C": "c", "D": "d"}, "correct_answer": "A", "explanation": "E"}]}'
    assert validate_json_response(valid_json)
    print("✓ JSON validation working correctly")
    
except Exception as e:
    print(f"✗ LLM handlers/utils failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: RAG module
print("\n[5/5] Testing RAG module...")
try:
    from RAG.retriever import Retriever
    print("✓ Retriever imported successfully")
    
    # Check that it has required methods
    required_methods = ['set_data', 'build_bm25', 'build_faiss_index', 'hybrid_search_RRF']
    for method in required_methods:
        assert hasattr(Retriever, method), f"Missing method: {method}"
    print("✓ Retriever has all required methods")
    
except Exception as e:
    print(f"✗ RAG module failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✓ ALL TESTS PASSED! REFACTOR SUCCESSFUL!")
print("=" * 60)
print("\n📁 New Structure:")
print("""
config/
  ├── __init__.py
  ├── config.py (Settings with Pydantic)
  └── constants.py (Global constants)

core/
  └── __init__.py (Pydantic models)

utils/
  └── __init__.py (Logger utility)

LLM/
  ├── handlers/
  │   ├── __init__.py
  │   ├── base_handler.py (BaseHandler ABC)
  │   ├── question_handler.py (QuestionGenerator)
  │   ├── response_handler.py (ResponseFormatter, AnswerScorer)
  │   └── fallback_handler.py (FallbackHandler)
  ├── __init__.py (Exports all modules)
  ├── prompts.py (All prompt templates)
  ├── validators.py (Input validation)
  ├── utils.py (Helper functions)
  └── context_analyzer.py (ContextAnalyzer)

RAG/
  ├── retriever.py (Improved with logging & type hints)
  └── ... (other modules)
""")

print("\n🎯 Key Improvements:")
print("✓ Centralized configuration management")
print("✓ Type safety with Pydantic models")
print("✓ Logging infrastructure across all modules")
print("✓ Separation of concerns (handlers pattern)")
print("✓ Reusable prompts and validators")
print("✓ Better error handling and logging")
print("✓ Comprehensive type hints")
