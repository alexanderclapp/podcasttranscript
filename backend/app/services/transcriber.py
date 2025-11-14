import os
from openai import OpenAI
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def transcribe_audio(audio_file_path: str, api_key: Optional[str] = None) -> str:
    """
    Transcribe audio file using OpenAI Whisper API.
    
    Args:
        audio_file_path: Path to audio file
        api_key: OpenAI API key (optional, can use env var)
        
    Returns:
        Transcript text
    """
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("OpenAI API key is required")
    
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
    try:
        logger.info(f"Starting transcription for file: {audio_file_path}")
        
        # Open the audio file
        with open(audio_file_path, 'rb') as audio_file:
            # Use Whisper API for transcription
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
        
        logger.info("Transcription completed successfully")
        return transcript
        
    except Exception as e:
        logger.error(f"Error during transcription: {str(e)}")
        raise Exception(f"Failed to transcribe audio: {str(e)}")

