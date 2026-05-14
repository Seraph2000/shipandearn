import hashlib
import config
from meo import storage

_client = None


def _get_client():
    global _client
    if _client is None:
        import anthropic
        _client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    return _client


def _cached_call(prompt: str) -> str:
    h = hashlib.sha256(prompt.encode()).hexdigest()
    cached = storage.get_ai_cached(h)
    if cached:
        return cached
    client = _get_client()
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    result = response.content[0].text
    storage.set_ai_cache(h, result)
    return result


def summarise_instructions(title: str, instructions: str) -> str:
    if not config.ANTHROPIC_API_KEY:
        return "AI not configured — add ANTHROPIC_API_KEY to .env"
    prompt = (
        f"Summarise these task instructions in 3 concise bullet points. "
        f"Plain text only, no preamble.\n\nTask: {title}\n\n{instructions}"
    )
    return _cached_call(prompt)


def draft_answers(title: str, questions: str) -> str:
    if not config.ANTHROPIC_API_KEY:
        return "AI not configured — add ANTHROPIC_API_KEY to .env"
    prompt = (
        f"Draft natural, concise answers for these questions. "
        f"Output as Q: / A: pairs only.\n\nContext: {title}\n\n{questions}"
    )
    return _cached_call(prompt)
