from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import base64
import uuid
import os

# -------------------------------
# App initialization
# -------------------------------
app = FastAPI()

SECRET_API_KEY = os.getenv("SECRET_API_KEY")

# -------------------------------
# Request model
# -------------------------------
class VoiceRequest(BaseModel):
    language: str
    audioFormat: str
    audioBase64: str


# -------------------------------
# Utility: Decode & save audio
# -------------------------------
def save_base64_audio(audio_base64: str, audio_format: str) -> str:
    """
    Decodes Base64 audio and saves it as a file.
    Returns the filename.
    """

    # 1️⃣ Validate audio format
    if audio_format.lower() != "mp3":
        raise HTTPException(status_code=400, detail="Only mp3 format is supported")

    # 2️⃣ Decode Base64
    try:
        audio_bytes = base64.b64decode(audio_base64)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Base64 audio")

    # 3️⃣ File size validation (max 5 MB)
    if len(audio_bytes) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Audio file too large")

    # 4️⃣ Save audio file
    filename = f"audio_{uuid.uuid4()}.mp3"
    with open(filename, "wb") as f:
        f.write(audio_bytes)

    return filename


# -------------------------------
# Rule-based "model"
# -------------------------------
def classify_audio_rule_based(file_path: str):
    """
    Rule-based voice classification using file size.
    """

    file_size_kb = os.path.getsize(file_path) / 1024

    if file_size_kb < 50:
        return {
            "classification": "AI_GENERATED",
            "confidence": 0.78,
            "explanation": (
                "The uploaded audio file is unusually small. "
                "AI-generated voices often produce compressed audio."
            )
        }

    return {
        "classification": "HUMAN",
        "confidence": 0.72,
        "explanation": (
            "The audio file size and structure are consistent "
            "with natural human speech."
        )
    }


# -------------------------------
# API Endpoint
# -------------------------------
@app.post("/api/voice-detection")
def detect_voice(
    data: VoiceRequest,
    x_api_key: str = Header(None)
):
    # 1️⃣ API key validation
    if x_api_key != SECRET_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    SUPPORTED_LANGUAGES = {
    "tamil",
    "english",
    "hindi",
    "malayalam",
    "telugu",
}


    if data.language.lower() not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail="Unsupported language"
        )

    # 2️⃣ Basic input validation
    if not data.audioBase64:
        raise HTTPException(status_code=400, detail="Audio data missing")

    # 3️⃣ Decode & save audio
    audio_file_path = save_base64_audio(
        data.audioBase64,
        data.audioFormat
    )

    # 4️⃣ Apply rule-based model
    result = classify_audio_rule_based(audio_file_path)

    # 5️⃣ Return response
    return {
        "status": "success",
        "language": data.language,
        "classification": result["classification"],
        "confidenceScore": result["confidence"],
        "explanation": result["explanation"]
    }

