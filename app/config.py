import os

class Config:
    # Model settings: use a local path or a model id (downloads on first run)
    HF_MODEL_ID = os.getenv("HF_MODEL_ID", "sshleifer/distilbart-cnn-12-6")
    HF_LOCAL_PATH = os.getenv("HF_LOCAL_PATH", "").strip() # e.g. "./models/distilbart-cnn-12-6"
    SUMMARY_TARGET_WORDS = int(os.getenv("SUMMARY_TARGET_WORDS", "140"))
    EXTRACT_MAX_CHARS = int(os.getenv("EXTRACT_MAX_CHARS", "20000"))

    # Trafilatura knobs (tuned for article/blog precision)
    TRAFILATURA_FAVOR_RECALL = bool(int(os.getenv("TRAFILATURA_FAVOR_RECALL", "0")))