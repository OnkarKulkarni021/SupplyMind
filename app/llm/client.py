from langchain_huggingface import HuggingFacePipeline
from transformers import pipeline

def get_llm():
    pipe = pipeline(
        "text2text-generation",
        model="google/flan-t5-small",
        max_new_tokens=200
    )

    return HuggingFacePipeline(pipeline=pipe)