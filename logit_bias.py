import openai
import tiktoken
from typing import List

class LogitBias:
    def __init__(self, api_key: str, model: str, suppressed_phrases: List[str], extra_suppressed_tokens: List[int], bias: int, request_timeout: int):
        self.api_key = api_key
        openai.api_key = self.api_key
        self.model = model
        self.suppressed_phrases = suppressed_phrases
        self.extra_suppressed_tokens = extra_suppressed_tokens
        self.bias = bias
        self.request_timeout = request_timeout
        self.encoding = tiktoken.encoding_for_model(self.model)
        self.logit_bias = self._create_logit_bias()


    def _augment_phrases(self, phrases: List[str]) -> List[str]:
        def _iter():
            for p in phrases:
                yield from (" " + p, p.lower(), p.upper(), p.capitalize(), p.title())
        return list(set(_iter()))

    def _create_logit_bias(self) -> dict:
        phrases = self._augment_phrases(self.suppressed_phrases)
        tokens = list(set([t for p in phrases for t in self.encoding.encode(p)]))
        tokens += self.extra_suppressed_tokens
        return {t: self.bias for t in tokens}

    def generate_responses(self, prompt: str, n_responses: int, temperature: float, system_message: str = None):
        for i in range(n_responses):
            response = self._complete(prompt, logit_bias=self.logit_bias, temperature=temperature, system_message=system_message, request_timeout=self.request_timeout)
            yield response

    def _complete(self, messages: list, model=None, system_message=None, **kwargs) -> str:
        if type(messages) == str:
            messages = [messages]
        chat_messages = [{"role": "user", "content": m} for m in messages if isinstance(m, str)]
        if system_message:
            chat_messages.insert(0, {"role": "system", "content": system_message})
        response = openai.ChatCompletion.create(model=model or self.model, messages=chat_messages, **kwargs)
        return response.choices[0].message.content
        
