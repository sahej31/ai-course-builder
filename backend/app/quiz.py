def quiz_prompt(topic: str, outline: str | list, context: str, num_q: int = 6):
    if isinstance(outline, list):
        outline_text = "\n".join(map(str, outline))
    else:
        outline_text = str(outline)

    return f"""
You are a strict quiz author. Create {num_q} MCQs (4 options each, one correct),
covering key facts and pitfalls from the outline below. Provide pure JSON with:
[{{ "question": "...", "options": ["A","B","C","D"], "answer_index": 0, "explanation": "..." }}...]

Topic: {topic}

Outline:
{outline_text}

Context (excerpts):
{context[:3000]}
""".strip()
