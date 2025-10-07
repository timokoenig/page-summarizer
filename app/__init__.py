import logging
import os
import threading
from flask import Flask
from .config import Config
from .routes import bp as routes_bp
from .services.summarizer import warmup_model, model_ready, model_error

def create_app() -> Flask:
    app = Flask(__name__, template_folder="../templates")
    app.config.from_object(Config)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
    app.logger.info("Starting Page Summarizer")

    app.register_blueprint(routes_bp)

    threading.Thread(target=warmup_model, daemon=True).start()

    @app.get("/health")
    def health():
        if model_error():
            return {"ready": False, "error": model_error()}, 500
        return {"ready": model_ready()}, 200 if model_ready() else 202

    return app