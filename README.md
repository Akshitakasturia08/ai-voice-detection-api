# AI Voice Detection API

## Problem Statement
This project is developed for **Problem 1 – AI for Fraud Detection & User Safety**.  
The objective is to determine whether a submitted voice sample is **AI-generated** or **Human** using a backend API.

---

## Solution Overview
The system provides a **REST API** built using **FastAPI** that:
- Accepts Base64-encoded audio files
- Validates requests using an API key
- Performs rule-based voice classification
- Returns classification results with confidence and explanation

The architecture is simple, secure, and designed to be easily extendable to ML-based models in the future.

---

## Technology Stack
- Python
- FastAPI
- Uvicorn
- REST API
- Base64 Encoding
- Swagger UI

---

## API Endpoint

### POST `/api/voice-detection`

#### Headers


Content-Type: application/json
x-api-key: my_secret_key_123


#### Request Body
```json
{
  "language": "English",
  "audioFormat": "mp3",
  "audioBase64": "BASE64_ENCODED_AUDIO"
}


#### Request Body
```json
{
  "language": "English",
  "audioFormat": "mp3",
  "audioBase64": "BASE64_ENCODED_AUDIO"
}

Response Body
{
  "status": "success",
  "language": "English",
  "classification": "AI_GENERATED",
  "confidenceScore": 0.78,
  "explanation": "Reason for classification"
}

Supported Languages
English
Hindi
Tamil
Telugu
Malayalam



Detection Logic

This prototype uses a rule-based detection approach:

Audio is decoded from Base64 format
File size is analyzed
Extremely small audio files are flagged as AI-generated
Larger audio samples are treated as Human speech
