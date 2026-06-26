from .manager import PromptManager, PromptTemplate, create_prompt

prompt_manager = PromptManager()

SYSTEM_PROMPT = prompt_manager.load('system')
SYSTEM_PROMPT_SHORT = prompt_manager.load('system_prompt_short')
INTENT_ROUTER_PROMPT = prompt_manager.load('intent_router')
PARAM_EXTRACT_PROMPT = prompt_manager.load('param_extract')
QUESTION_GENERATION_PROMPT = prompt_manager.load('question_generation')
ESSAY_GENERATION_PROMPT = prompt_manager.load('essay_generation')
FILL_BLANK_GENERATION_PROMPT = prompt_manager.load('fill_blank_generation')
TRUE_FALSE_GENERATION_PROMPT = prompt_manager.load('true_false_generation')
ESSAY_SCORING_PROMPT = prompt_manager.load('essay_scoring')
UTILITY_SCORING_PROMPT = prompt_manager.load('utility_scoring')
QUESTION_VALIDATION_PROMPT = prompt_manager.load('question_validation')
SLIDE_OUTLINE_PROMPT = prompt_manager.load('slide_outline')
SLIDE_CONTENT_PROMPT = prompt_manager.load('slide_content')
SLIDE_QUIZ_PROMPT = prompt_manager.load('slide_quiz')
SLIDE_MEDIA_PROMPT = prompt_manager.load('slide_media')
LESSON_PLAN_OUTLINE_PROMPT = prompt_manager.load('lesson_plan_outline')
LESSON_PLAN_CONTENT_PROMPT = prompt_manager.load('lesson_plan_content')
LESSON_PLAN_OUTLINE_CONTEXT_PROMPT = prompt_manager.load('lesson_plan_outline_context')
QUALITY_REVISION_INSTRUCTION_PROMPT = prompt_manager.load('quality_revision_instruction')
CHAT_PROMPT = prompt_manager.load('chat')
EXPLAIN_PROMPT = prompt_manager.load('explain')
EVALUATION_ANSWER_PROMPT = prompt_manager.load('evaluation_answer')
EXTRACT_PROMPT = prompt_manager.load('extract')
FALLBACK_PROMPT = prompt_manager.load('fallback')
FEEDBACK_GENERATION_PROMPT = prompt_manager.load('feedback_generation')
RESPONSE_FORMATTING_PROMPT = prompt_manager.load('response_formatting')
KNOWLEDGE_RELATION_PROMPT = prompt_manager.load('knowledge_relation')
QUERY_REWRITE_PROMPT = prompt_manager.load('query_rewrite')
CONTEXT_BUILD_PROMPT = prompt_manager.load('context_build')
SUPERVISOR_SYSTEM_PROMPT = prompt_manager.load('supervisor_system')
SUPERVISOR_USER_PROMPT = prompt_manager.load('supervisor_user')
SUPERVISOR_AFTER_OUTLINE_PROMPT = prompt_manager.load('supervisor_after_outline')
SUPERVISOR_AFTER_CONTENT_PROMPT = prompt_manager.load('supervisor_after_content')
SUPERVISOR_REVISION_REQUEST_PROMPT = prompt_manager.load('supervisor_revision_request')
QUIZ_REVISION_QUERY_PROMPT = prompt_manager.load('quiz_revision_query')
QUALITY_REVIEW_JSON_CONTRACT = prompt_manager.load('quality_review_json_contract')
QUIZ_QUALITY_REVIEW_PROMPT = prompt_manager.load('quiz_quality_review')
SLIDE_QUALITY_REVIEW_PROMPT = prompt_manager.load('slide_quality_review')
LESSON_PLAN_QUALITY_REVIEW_PROMPT = prompt_manager.load('lesson_plan_quality_review')

QUESTION_GENERATION_TEMPLATE = create_prompt(
    name='question_generation',
    template=QUESTION_GENERATION_PROMPT,
    required_vars=['query', 'context', 'num_questions', 'difficulty'],
    version='1.1',
    description='Generate multiple choice questions from retrieved context',
)

ESSAY_GENERATION_TEMPLATE = create_prompt(
    name='essay_generation',
    template=ESSAY_GENERATION_PROMPT,
    required_vars=['query', 'context', 'num_questions', 'difficulty'],
    version='1.0',
    description='Generate essay questions with sample answers and rubrics',
)

FILL_BLANK_GENERATION_TEMPLATE = create_prompt(
    name='fill_blank_generation',
    template=FILL_BLANK_GENERATION_PROMPT,
    required_vars=['query', 'context', 'num_questions', 'difficulty'],
    version='1.0',
    description='Generate fill-in-the-blank questions',
)

TRUE_FALSE_GENERATION_TEMPLATE = create_prompt(
    name='true_false_generation',
    template=TRUE_FALSE_GENERATION_PROMPT,
    required_vars=['query', 'context', 'num_questions', 'difficulty'],
    version='1.0',
    description='Generate true/false questions',
)

ESSAY_SCORING_TEMPLATE = create_prompt(
    name='essay_scoring',
    template=ESSAY_SCORING_PROMPT,
    required_vars=['question', 'sample_answer', 'rubric', 'user_answer'],
    version='1.0',
    description='Score essay answers using LLM based on rubrics',
)

SCORING_TEMPLATE = create_prompt(
    name='answer_scoring',
    template=UTILITY_SCORING_PROMPT,
    required_vars=['state_text', 'query'],
    version='1.0',
    description="Score user's answer against stored questions",
)

QUESTION_VALIDATION_TEMPLATE = create_prompt(
    name='question_validation',
    template=QUESTION_VALIDATION_PROMPT,
    required_vars=['question_type', 'context', 'questions_json'],
    version='1.0',
    description='LLM Node #2: Validate generated questions against source context',
)

SLIDE_OUTLINE_TEMPLATE = create_prompt(
    name='slide_outline',
    template=SLIDE_OUTLINE_PROMPT,
    required_vars=['topic', 'grade', 'book', 'context_map'],
    version='1.0',
    description='Agent 2: Generate slide outline (8-12 slides) from structured context',
)

SLIDE_CONTENT_TEMPLATE = create_prompt(
    name='slide_content',
    template=SLIDE_CONTENT_PROMPT,
    required_vars=['slide_id', 'slide_type', 'slide_title', 'slide_objective', 'key_points', 'context_subset'],
    version='1.0',
    description='Agent 3: Write detailed content for a single slide',
)

SLIDE_QUIZ_TEMPLATE = create_prompt(
    name='slide_quiz',
    template=SLIDE_QUIZ_PROMPT,
    required_vars=['topic', 'context'],
    version='1.0',
    description='Agent 4: Generate 3-5 MCQ quiz items for slide exercises',
)

SLIDE_MEDIA_TEMPLATE = create_prompt(
    name='slide_media',
    template=SLIDE_MEDIA_PROMPT,
    required_vars=['topic', 'grade', 'book', 'slide_plan'],
    version='1.0',
    description='Agent 1: Suggest media captions for slide illustrations',
)

PARAM_EXTRACT_TEMPLATE = create_prompt(
    name='param_extract',
    template=PARAM_EXTRACT_PROMPT,
    required_vars=['query', 'enriched_query', 'rag_queries', 'history_context'],
    version='1.0',
    description='Extract shared request parameters for all services',
)

LESSON_PLAN_OUTLINE_TEMPLATE = create_prompt(
    name='lesson_plan_outline',
    template=LESSON_PLAN_OUTLINE_PROMPT,
    required_vars=['topic', 'grade', 'book', 'context_map'],
    version='1.0',
    description='Generate lesson plan outline (7-10 sections) following Vietnamese education standards',
)

LESSON_PLAN_CONTENT_TEMPLATE = create_prompt(
    name='lesson_plan_content',
    template=LESSON_PLAN_CONTENT_PROMPT,
    required_vars=['slide_id', 'slide_type', 'slide_title', 'slide_objective', 'key_points', 'context_subset'],
    version='1.0',
    description='Write detailed content for a lesson plan section',
)

EXTRACT_TEMPLATE = create_prompt(
    name='extract_metadata',
    template=EXTRACT_PROMPT,
    required_vars=['query'],
    version='1.0',
    description='Extract metadata (lesson, grade, topic) from user query',
)

FALLBACK_TEMPLATE = create_prompt(
    name='fallback',
    template=FALLBACK_PROMPT,
    required_vars=['query'],
    version='1.0',
    description='Handle off-topic or chitchat queries',
)

QUERY_REWRITE_TEMPLATE = create_prompt(
    name='query_rewrite',
    template=QUERY_REWRITE_PROMPT,
    required_vars=['query', 'context'],
    version='1.0',
    description='Rewrite ambiguous queries using conversation context into 2-3 standalone search queries',
)

CONTEXT_BUILD_TEMPLATE = create_prompt(
    name='context_builder',
    template=CONTEXT_BUILD_PROMPT,
    required_vars=['query', 'raw_context', 'task_description', 'num_chunks'],
    version='1.0',
    description='Synthesize multiple RAG chunks into a single coherent context for downstream LLM calls',
)

__all__ = ['PromptManager', 'PromptTemplate', 'create_prompt', 'prompt_manager', 'SYSTEM_PROMPT', 'SYSTEM_PROMPT_SHORT', 'INTENT_ROUTER_PROMPT', 'PARAM_EXTRACT_PROMPT', 'PARAM_EXTRACT_TEMPLATE', 'QUESTION_GENERATION_PROMPT', 'QUESTION_GENERATION_TEMPLATE', 'ESSAY_GENERATION_PROMPT', 'ESSAY_GENERATION_TEMPLATE', 'FILL_BLANK_GENERATION_PROMPT', 'FILL_BLANK_GENERATION_TEMPLATE', 'TRUE_FALSE_GENERATION_PROMPT', 'TRUE_FALSE_GENERATION_TEMPLATE', 'ESSAY_SCORING_PROMPT', 'ESSAY_SCORING_TEMPLATE', 'UTILITY_SCORING_PROMPT', 'SCORING_TEMPLATE', 'QUESTION_VALIDATION_PROMPT', 'QUESTION_VALIDATION_TEMPLATE', 'SLIDE_OUTLINE_PROMPT', 'SLIDE_OUTLINE_TEMPLATE', 'SLIDE_CONTENT_PROMPT', 'SLIDE_CONTENT_TEMPLATE', 'SLIDE_QUIZ_PROMPT', 'SLIDE_QUIZ_TEMPLATE', 'SLIDE_MEDIA_PROMPT', 'SLIDE_MEDIA_TEMPLATE', 'LESSON_PLAN_OUTLINE_PROMPT', 'LESSON_PLAN_OUTLINE_TEMPLATE', 'LESSON_PLAN_CONTENT_PROMPT', 'LESSON_PLAN_CONTENT_TEMPLATE', 'LESSON_PLAN_OUTLINE_CONTEXT_PROMPT', 'QUALITY_REVISION_INSTRUCTION_PROMPT', 'CHAT_PROMPT', 'EXPLAIN_PROMPT', 'EVALUATION_ANSWER_PROMPT', 'EXTRACT_PROMPT', 'EXTRACT_TEMPLATE', 'FALLBACK_PROMPT', 'FALLBACK_TEMPLATE', 'FEEDBACK_GENERATION_PROMPT', 'RESPONSE_FORMATTING_PROMPT', 'KNOWLEDGE_RELATION_PROMPT', 'QUERY_REWRITE_PROMPT', 'QUERY_REWRITE_TEMPLATE', 'CONTEXT_BUILD_PROMPT', 'CONTEXT_BUILD_TEMPLATE', 'SUPERVISOR_SYSTEM_PROMPT', 'SUPERVISOR_USER_PROMPT', 'SUPERVISOR_AFTER_OUTLINE_PROMPT', 'SUPERVISOR_AFTER_CONTENT_PROMPT', 'SUPERVISOR_REVISION_REQUEST_PROMPT', 'QUIZ_REVISION_QUERY_PROMPT', 'QUALITY_REVIEW_JSON_CONTRACT', 'QUIZ_QUALITY_REVIEW_PROMPT', 'SLIDE_QUALITY_REVIEW_PROMPT', 'LESSON_PLAN_QUALITY_REVIEW_PROMPT']
