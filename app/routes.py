from flask import Blueprint, jsonify, render_template, request, current_app
from .services.extractor import extract_main_content, is_valid_url
from .services.summarizer import summarize_text, model_ready, model_error

bp = Blueprint("routes", __name__)

@bp.get("/")
def index():
    return render_template("index.html")

@bp.post("/submit")
def submit():
    data = request.get_json(silent=True) or {}
    url = (data.get("url") or "").strip()

    if not is_valid_url(url):
        return jsonify({"error": "Please provide a valid http(s) URL."}), 400

    if not model_ready() and not model_error():
        return jsonify({"error": "Model is downloading/initializing. Try again shortly."}), 503

    if model_error():
        return jsonify({"error": f"Model failed to initialize: {model_error()}"}), 500

    try:
        content = extract_main_content(
            url,
            favor_recall=current_app.config["TRAFILATURA_FAVOR_RECALL"]
        )
        if not content:
            return jsonify({"error": "Could not extract main content from the URL."}), 422

        # Keep summarization fast & bounded
        max_chars = current_app.config["EXTRACT_MAX_CHARS"]
        if len(content) > max_chars:
            content = content[:max_chars]

        summary = summarize_text(
            content,
            target_words=current_app.config["SUMMARY_TARGET_WORDS"]
        )
        return jsonify({"message": summary})
    except Exception as e:
        current_app.logger.exception("Processing failed")
        return jsonify({"error": "Processing failed.", "detail": str(e)}), 500