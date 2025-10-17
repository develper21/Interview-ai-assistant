# main.py

import os
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

# Google ki libraries
import google.generativeai as genai
from google.cloud import speech

# Environment variables load karein
load_dotenv()

# FastAPI application initialize karein
app = FastAPI()

# --- API Clients Configuration ---

# 1. Gemini Pro Client Setup
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
gemini_model = genai.GenerativeModel('gemini-pro')

# 2. Google Speech-to-Text Client Setup
# Yahan hum maan rahe hain ki GOOGLE_APPLICATION_CREDENTIALS set hai
speech_client = speech.SpeechClient()

# --- WebSocket Communication Logic ---

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Yeh function frontend se WebSocket connection handle karega.
    """
    await websocket.accept()
    print("Client connected!")

    # Google STT ke liye streaming config
    streaming_config = speech.StreamingRecognitionConfig(
        config=speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS, # Frontend se is format mein bhejenge
            sample_rate_hertz=48000,
            language_code="en-US",
            enable_automatic_punctuation=True,
        ),
        interim_results=True,
    )

    try:
        # Audio stream ko handle karne ke liye ek generator function banayenge
        async def audio_stream_generator():
            while True:
                # Frontend se audio chunk (bytes) receive karein
                audio_chunk = await websocket.receive_bytes()
                yield speech.StreamingRecognizeRequest(audio_content=audio_chunk)

        # STT API se responses receive karein
        responses = speech_client.streaming_recognize(
            config=streaming_config,
            requests=audio_stream_generator()
        )

        for response in responses:
            if not response.results:
                continue

            result = response.results[0]
            if not result.alternatives:
                continue

            transcript = result.alternatives[0].transcript

            # Agar yeh final transcript hai (is_final=true)
            if result.is_final:
                print(f"Final Transcript: {transcript}")

                # Ab is transcript ko Gemini ko bhejenge
                # Ek accha prompt banayein
                prompt = f"""
                You are an expert interview assistant.
                The user was asked the following question: "{transcript}"
                Provide a concise and helpful answer in 3-4 bullet points.
                The response should be directly useful to the user in a live interview.
                """

                # Gemini se response generate karein
                gemini_response = gemini_model.generate_content(prompt)

                # Frontend ko suggestion bhejein
                await websocket.send_json({
                    "type": "suggestion",
                    "text": gemini_response.text
                })

            else:
                # Interim (beech ka) result frontend ko bhej sakte hain (optional)
                await websocket.send_json({
                    "type": "transcript",
                    "text": transcript
                })


    except WebSocketDisconnect:
        print("Client disconnected.")
    except Exception as e:
        print(f"An error occurred: {e}")
        await websocket.close(code=1011, reason=str(e))

# --- Server Run Command ---
# Is server ko chalane ke liye terminal mein yeh command likhein:
# uvicorn main:app --reload
