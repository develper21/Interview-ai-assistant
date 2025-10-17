"""
Enhanced Speech-to-Text service for interview audio processing
"""

import asyncio
import io
from typing import AsyncGenerator, Dict, List, Optional, Any
from datetime import datetime
import google.cloud.speech as speech
from google.oauth2 import service_account

from core.config import settings
from api.v1.schemas.websocket_models import TranscriptMessage


class STTService:
    """Enhanced Speech-to-Text service"""

    def __init__(self):
        """Initialize STT service"""
        if not settings.google_speech_credentials_path:
            # Use default credentials if no service account file specified
            self.client = speech.SpeechClient()
        else:
            # Use service account credentials
            credentials = service_account.Credentials.from_service_account_file(
                settings.google_speech_credentials_path
            )
            self.client = speech.SpeechClient(credentials=credentials)

    def create_streaming_config(
        self,
        sample_rate: int = 16000,
        language_code: str = "en-US",
        enable_automatic_punctuation: bool = True,
        enable_word_time_offsets: bool = True,
        max_alternatives: int = 1,
        model: str = "latest_long"
    ) -> speech.StreamingRecognitionConfig:
        """Create streaming recognition configuration"""

        return speech.StreamingRecognitionConfig(
            config=speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=sample_rate,
                language_code=language_code,
                enable_automatic_punctuation=enable_automatic_punctuation,
                enable_word_time_offsets=enable_word_time_offsets,
                max_alternatives=max_alternatives,
                model=model,
                use_enhanced=True,  # Use enhanced models for better accuracy
            ),
            interim_results=True,
        )

    async def transcribe_audio_stream(
        self,
        audio_generator: AsyncGenerator[bytes, None],
        sample_rate: int = 16000,
        language_code: str = "en-US"
    ) -> AsyncGenerator[TranscriptMessage, None]:
        """Transcribe audio stream and yield transcript messages"""

        # Create streaming config
        streaming_config = self.create_streaming_config(
            sample_rate=sample_rate,
            language_code=language_code
        )

        # Create request generator
        async def request_generator():
            async for audio_chunk in audio_generator:
                if audio_chunk:
                    yield speech.StreamingRecognizeRequest(audio_content=audio_chunk)

        try:
            # Start streaming recognition
            responses = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.streaming_recognize(
                    config=streaming_config,
                    requests=request_generator()
                )
            )

            current_transcript = ""
            confidence_score = 0.0

            # Process responses
            for response in responses:
                if not response.results:
                    continue

                result = response.results[0]

                if not result.alternatives:
                    continue

                alternative = result.alternatives[0]
                transcript = alternative.transcript
                confidence = alternative.confidence if alternative.confidence else 0.0

                # Update current transcript
                if result.is_final:
                    current_transcript = transcript
                    confidence_score = confidence

                    yield TranscriptMessage(
                        type="transcript_update",
                        timestamp=datetime.now().timestamp(),
                        transcript=current_transcript,
                        is_final=True,
                        confidence=confidence_score
                    )

                else:
                    # Update interim transcript
                    current_transcript = transcript

                    yield TranscriptMessage(
                        type="transcript_update",
                        timestamp=datetime.now().timestamp(),
                        transcript=current_transcript,
                        is_final=False,
                        confidence=confidence
                    )

        except Exception as e:
            print(f"STT Error: {e}")
            yield TranscriptMessage(
                type="error",
                timestamp=datetime.now().timestamp(),
                transcript="",
                is_final=False,
                confidence=0.0
            )

    async def transcribe_audio_file(
        self,
        audio_data: bytes,
        sample_rate: int = 16000,
        language_code: str = "en-US"
    ) -> Dict[str, Any]:
        """Transcribe audio file data"""

        try:
            # Create audio object
            audio = speech.RecognitionAudio(content=audio_data)

            # Create config
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=sample_rate,
                language_code=language_code,
                enable_automatic_punctuation=True,
                enable_word_time_offsets=True,
                max_alternatives=3,
                model="latest_long",
                use_enhanced=True,
            )

            # Perform recognition
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.recognize(config=config, audio=audio)
            )

            if not response.results:
                return {
                    "transcript": "",
                    "confidence": 0.0,
                    "alternatives": []
                }

            result = response.results[0]
            transcript = result.alternatives[0].transcript
            confidence = result.alternatives[0].confidence if result.alternatives[0].confidence else 0.0

            alternatives = [
                {
                    "transcript": alt.transcript,
                    "confidence": alt.confidence if alt.confidence else 0.0
                }
                for alt in result.alternatives
            ]

            return {
                "transcript": transcript,
                "confidence": confidence,
                "alternatives": alternatives,
                "word_time_offsets": [
                    {
                        "word": word.word,
                        "start_time": word.start_time.total_seconds() if word.start_time else 0,
                        "end_time": word.end_time.total_seconds() if word.end_time else 0
                    }
                    for word in result.alternatives[0].words
                ] if result.alternatives[0].words else []
            }

        except Exception as e:
            print(f"STT File Error: {e}")
            return {
                "transcript": "",
                "confidence": 0.0,
                "alternatives": [],
                "error": str(e)
            }

    async def get_supported_languages(self) -> List[Dict[str, str]]:
        """Get list of supported languages for speech recognition"""

        try:
            # This would typically come from Google's documentation or API
            # For now, returning commonly supported languages
            return [
                {"code": "en-US", "name": "English (US)"},
                {"code": "en-GB", "name": "English (UK)"},
                {"code": "es-ES", "name": "Spanish (Spain)"},
                {"code": "es-US", "name": "Spanish (US)"},
                {"code": "fr-FR", "name": "French (France)"},
                {"code": "de-DE", "name": "German (Germany)"},
                {"code": "it-IT", "name": "Italian (Italy)"},
                {"code": "pt-BR", "name": "Portuguese (Brazil)"},
                {"code": "ru-RU", "name": "Russian (Russia)"},
                {"code": "ja-JP", "name": "Japanese (Japan)"},
                {"code": "ko-KR", "name": "Korean (Korea)"},
                {"code": "zh-CN", "name": "Chinese (Mandarin, Simplified)"},
                {"code": "hi-IN", "name": "Hindi (India)"},
                {"code": "ar-SA", "name": "Arabic (Saudi Arabia)"}
            ]

        except Exception as e:
            print(f"Error getting supported languages: {e}")
            return []

    async def analyze_audio_quality(
        self,
        audio_data: bytes,
        sample_rate: int = 16000
    ) -> Dict[str, Any]:
        """Analyze audio quality for better recognition"""

        try:
            # Basic audio analysis
            audio_size = len(audio_data)
            duration_seconds = audio_size / (sample_rate * 2)  # Assuming 16-bit samples

            # Check for silence or very low volume
            # This is a simplified check - in production, you'd use proper audio analysis
            max_amplitude = max(audio_data[i] for i in range(0, min(len(audio_data), 1000), 2))

            quality_score = 100
            issues = []

            if duration_seconds < 1:
                quality_score -= 30
                issues.append("Audio too short")

            if max_amplitude < 1000:  # Very low amplitude threshold
                quality_score -= 40
                issues.append("Audio volume too low")

            if duration_seconds > 300:  # 5 minutes
                quality_score -= 20
                issues.append("Audio too long for optimal processing")

            return {
                "quality_score": max(0, quality_score),
                "duration_seconds": duration_seconds,
                "file_size_bytes": audio_size,
                "sample_rate": sample_rate,
                "issues": issues,
                "recommendations": [
                    "Speak clearly and at moderate volume",
                    "Minimize background noise",
                    "Keep responses concise but complete"
                ]
            }

        except Exception as e:
            print(f"Error analyzing audio quality: {e}")
            return {
                "quality_score": 50,
                "error": str(e)
            }


# Global service instance
stt_service = None

def get_stt_service() -> STTService:
    """Get or create STT service instance"""
    global stt_service
    if stt_service is None:
        stt_service = STTService()
    return stt_service


class MockSTTService:
    """Mock STT service for testing"""

    async def transcribe_audio_stream(self, *args, **kwargs):
        # Simulate processing delay
        await asyncio.sleep(0.1)
        yield TranscriptMessage(
            type="transcript_update",
            timestamp=datetime.now().timestamp(),
            transcript="Mock transcript for testing",
            is_final=True,
            confidence=0.85
        )

    async def transcribe_audio_file(self, *args, **kwargs):
        await asyncio.sleep(0.1)
        return {
            "transcript": "Mock transcript for testing",
            "confidence": 0.85,
            "alternatives": [
                {"transcript": "Mock transcript", "confidence": 0.85}
            ]
        }

    async def get_supported_languages(self):
        return [
            {"code": "en-US", "name": "English (US)"},
            {"code": "es-ES", "name": "Spanish (Spain)"}
        ]

    async def analyze_audio_quality(self, *args, **kwargs):
        return {
            "quality_score": 85,
            "duration_seconds": 10.0,
            "file_size_bytes": 320000,
            "sample_rate": 16000,
            "issues": [],
            "recommendations": ["Good audio quality"]
        }
