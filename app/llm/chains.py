from app.llm.client import get_llm
from app.llm.prompts import EXPLANATION_PROMPT

def generate_explanation(data):
    llm = get_llm()

    prompt = EXPLANATION_PROMPT.format(**data)

    response = llm.invoke(prompt)

    return response.content