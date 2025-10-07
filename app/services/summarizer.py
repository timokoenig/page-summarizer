import math
import os
from functools import lru_cache
from typing import Optional

MODEL_READY = False
MODEL_ERROR: Optional[str] = None

def model_ready() -> bool:
    return MODEL_READY

def model_error() -> Optional[str]:
    return MODEL_ERROR

def _local_or_id() -> str:
    local = os.getenv("HF_LOCAL_PATH", "").strip()
    return local if local else os.getenv("HF_MODEL_ID", "sshleifer/distilbart-cnn-12-6")

@lru_cache(maxsize=1)
def _hf_pipeline():
    from transformers import pipeline
    import torch
    model_or_path = _local_or_id()
    device = 0 if torch.cuda.is_available() else -1  # CPU if no GPU; no accelerate needed
    return pipeline(
        "summarization",
        model=model_or_path,
        tokenizer=model_or_path,
        device=device
    )

def warmup_model():
    global MODEL_READY, MODEL_ERROR
    try:
        pipe = _hf_pipeline()
        # Short warmup inference to load weights
        pipe("Warmup.", max_length=5, min_length=5)
        MODEL_READY = True
    except Exception as e:
        MODEL_ERROR = str(e)
        MODEL_READY = False

def summarize_with_hf(text: str, target_words: int = 140) -> str:
    pipe = _hf_pipeline()
    # Chunk roughly under 3k chars (≈ 1024 tokens safety for DistilBART)
    CHUNK_SIZE = 3000
    chunks = [text[i:i+CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE)] or [text]

    partial = []
    for ch in chunks:
        out = pipe(
            ch,
            max_length=max(60, math.ceil(target_words * 1.6)),
            min_length=max(20, math.ceil(target_words * 0.5)),
            do_sample=False,
        )[0]["summary_text"].strip()
        partial.append(out)

    combined = " ".join(partial)
    if len(chunks) > 1 and len(combined) > 1200:
        combined = pipe(
            combined,
            max_length=max(60, math.ceil(target_words * 1.6)),
            min_length=max(20, math.ceil(target_words * 0.5)),
            do_sample=False,
        )[0]["summary_text"].strip()
    return combined

# ---- Lightweight extractive fallback ----
import re
def summarize_extractive(text: str, sentences: int = 6) -> str:
    sents = re.split(r'(?<=[.!?])\s+', text)
    uniq = []
    seen = set()
    for s in sents:
        k = s.strip().lower()
        if k and k not in seen:
            uniq.append(s.strip())
            seen.add(k)
        if len(uniq) >= sentences:
            break
    return " ".join(uniq) if uniq else text[:500]

def summarize_text(text: str, target_words: int = 140) -> str:
    if not text or len(text) < 200:
        return text or "No readable content found on the page."
    try:
        return summarize_with_hf(text, target_words)
    except Exception:
        # If HF/torch fails for any reason, degrade gracefully
        return summarize_extractive(text, sentences=6)