# 📰 Page Summarizer

**Paste a URL. Get the gist—fast.**  
Page Summarizer fetches a webpage, extracts its main content, and generates a concise summary using a local AI model.

## ✨ Features

- 🧭 URL input → server fetches and extracts the **main article text**
- 🧠 Local summarization with **Hugging Face Transformers** (DistilBART by default)
- ⚡ Background **model warmup** to avoid slow first requests
- 🛡️ Graceful fallbacks and clear error messages
- 🎨 Minimal UI built with **Tailwind + React (via CDN)**

## 🚀 Quick Start

> **Python 3.10+** is recommended. Use a virtual environment.

```bash
git clone <this-repo>
cd page-summarizer
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

pip install --upgrade pip
pip install -r requirements.txt
```

Run the development server:

```bash
python run.py
# Open http://127.0.0.1:5000
```

> 💡 On the first run with a new model ID, the model files will be downloaded automatically.  
> To avoid runtime downloads, pre-download the model and set `HF_LOCAL_PATH` (see below).

## ⚙️ Configuration

Copy `.env.example` → `.env` (or set environment variables manually):

| Variable                     | Description                                                                       |
| ---------------------------- | --------------------------------------------------------------------------------- |
| **HF_LOCAL_PATH**            | Local folder containing a downloaded model (preferred for offline / fast startup) |
| **HF_MODEL_ID**              | Hugging Face model ID (e.g. `sshleifer/distilbart-cnn-12-6`)                      |
| **SUMMARY_TARGET_WORDS**     | Target summary length (approximate, in words)                                     |
| **EXTRACT_MAX_CHARS**        | Maximum input length to keep latency reasonable                                   |
| **TRAFILATURA_FAVOR_RECALL** | Set to `1` to capture more text on complex pages                                  |

## 📦 Pre-download the Model (Recommended)

```bash
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

## 🐳 Docker Setup

Run Page Summarizer in a container without installing Python locally.

### 1️⃣ Build the image

```bash
docker build -t page-summarizer .
```

(Make sure you’re in the project root with the `Dockerfile`.)

### 2️⃣ Run the container

```bash
docker run -p 5000:5000   --env-file .env   -v "$(pwd)/models:/app/models"   page-summarizer
```

**Explanation:**

| Flag                             | Description                                                        |
| -------------------------------- | ------------------------------------------------------------------ |
| `-p 5000:5000`                   | Exposes the app on [http://localhost:5000](http://localhost:5000)  |
| `--env-file .env`                | Loads environment variables like `HF_LOCAL_PATH`                   |
| `-v "$(pwd)/models:/app/models"` | Mounts your local model directory for faster startup & offline use |
| `page-summarizer`                | The Docker image name built above                                  |

> 🕐 If the model isn’t downloaded yet, the container will fetch it on first run (may take a minute).

## 🧩 Tech Stack

- **Backend:** Flask + Hugging Face Transformers
- **Frontend:** TailwindCSS + React (via CDN)
- **Extraction:** Trafilatura
- **Deployment:** Docker / local Python

## 🪪 License

MIT License © 2025
