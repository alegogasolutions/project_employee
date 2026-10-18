
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
_configured = False


def configurar_gemini_api_key() -> None:
    global _configured

    if _configured:
        return

    load_dotenv(BASE_DIR / ".env")

    if not os.getenv("GEMINI_API_KEY"):
        raise RuntimeError(
            "No se encuentra GEMINI_API_KEY en el archivo .env"
        )

    _configured = True