# Format context for prompt

def format_context(contexts, max_sections=None):
    formatted_sections = []
    
    sections_to_use = contexts if max_sections is None else contexts[:max_sections]
    
    for i, ctx in enumerate(sections_to_use, 1):
        metadata = ctx.get('metadata', {})
        section_text = (
            f"---\n"
            f"Title: {metadata.get('title', '')}\n"
            f"Level: {metadata.get('level', '')}\n"
            f"Type: {metadata.get('type', '')}\n"
            f"Context: {ctx.get('context', '')}\n"
            f"Content: {ctx.get('content', '')}\n"
        )
        formatted_sections.append(section_text)
    
    return "\n".join(formatted_sections)
