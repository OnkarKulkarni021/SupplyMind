from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from langchain_core.language_models.llms import LLM
from typing import Optional, List

model_name = "google/flan-t5-small"
_tokenizer = AutoTokenizer.from_pretrained(model_name)
_model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

class FlanT5LLM(LLM):
    @property
    def _llm_type(self) -> str:
        return "flan-t5"

    def _call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs) -> str:
        inputs = _tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
        outputs = _model.generate(**inputs, max_new_tokens=100)
        return _tokenizer.decode(outputs[0], skip_special_tokens=True)

llm = FlanT5LLM()

def get_llm():
    return llm