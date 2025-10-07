# Page Summarizer

**Paste a URL. Get the gist—fast.**  
Page Summarizer fetches a webpage, extracts the main content, and generates a concise summary using a local AI model.

## Features

- 🧭 URL input → server fetches and extracts the **main article text**
- 🧠 Local summarization with **Hugging Face Transformers** (DistilBART by default)
- ⚡ Background **model warmup** to avoid slow first requests
- 🛡️ Graceful fallbacks and clear error messages
- 🎨 Minimal UI with Tailwind + React (via CDN)

## Quick Start

> Python 3.10+ recommended. Use a virtual environment.

```sh
git clone <this-repo>
cd page-summarizer
python -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

Run (development)

```sh
python run.py
# open http://127.0.0.1:5000
```

On the very first run using a model id, the server may download model files.
You can pre-download and point HF_LOCAL_PATH to avoid runtime downloads (see below).

## Configuration

Copy .env.example to .env (or set env vars in your shell):

    •	HF_LOCAL_PATH — local folder containing a downloaded model (preferred for offline/fast startup)
    •	HF_MODEL_ID — HF Hub model id (e.g., sshleifer/distilbart-cnn-12-6)
    •	SUMMARY_TARGET_WORDS — target summary length in words (approximate)
    •	EXTRACT_MAX_CHARS — cap input length to keep latency in check
    •	TRAFILATURA_FAVOR_RECALL — set to 1 to capture more text on tricky pages

## Pre-download the model (recommended)

```sh
pip install huggingface_hub
python - <<'PY'
from huggingface_hub import snapshot_download
snapshot_download(
  repo_id="sshleifer/distilbart-cnn-12-6",
  local_dir="models/distilbart-cnn-12-6",
  local_dir_use_symlinks=False
)
print("Downloaded to models/distilbart-cnn-12-6")
PY

# Then set:
# export HF_LOCAL_PATH=./models/distilbart-cnn-12-6
```

## Docker

You can build and run Page Summarizer in a container without installing Python locally.

1. Build the image

```sh
docker build -t page-summarizer .
```

(Make sure you’re in the project root where the Dockerfile is.)

2. Run the container

```sh
docker run -p 5000:5000 \
 --env-file .env \
 -v "$(pwd)/models:/app/models" \
 page-summarizer
```

Explanation

    • -p 5000:5000 — exposes the app on http://localhost:5000
    • --env-file .env — loads your environment variables (like HF_LOCAL_PATH)
    • -v "$(pwd)/models:/app/models" — mounts your local model directory for faster startup and offline use
    • page-summarizer — the image name built above

If you haven’t downloaded the model yet, the container will fetch it the first time (it can take a minute).
