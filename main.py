from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import base64
import uuid
import os

# -------------------------------
# App initialization
# -------------------------------
app = FastAPI(title="AI Voice Detection API")

# Read API key from environment (Render)
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
    try:
        audio_bytes = base64.b64decode(audio_base64)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64 audio")

    filename = f"audio_{uuid.uuid4()}.{audio_format}"
    with open(filename, "wb") as f:
        f.write(audio_bytes)

    return filename


# -------------------------------
# Health check (VERY IMPORTANT)
# -------------------------------
@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "AI Voice Detection API is running"
    }


# -------------------------------
# Main API endpoint
# -------------------------------
@app.post("/detect")
def detect_voice(
    request: VoiceRequest,
    x_api_key: str = Header(None)
):
    # Check API key
    if not SECRET_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Server API key not configured"
        )

    if x_api_key != SECRET_API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )

    # Save audio
    filename = save_base64_audio(
        request.audioBase64,
        request.audioFormat
    )

    # ---- MOCK AI LOGIC (for hackathon/demo) ----
    confidence_score = 0.78
    classification = "AI_GENERATED"

    explanation = (
        "The uploaded audio is unusually small and compressed. "
        "AI-generated voices often show such patterns."
    )

    return {
        "status": "success",
        "language": request.language,
        "classification": classification,
        "confidenceScore": confidence_score,
        "explanation": explanation,
        "savedFile": filename
    }



