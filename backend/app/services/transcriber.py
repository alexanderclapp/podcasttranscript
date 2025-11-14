import os
from openai import OpenAI
from typing import Optional
import logging
import subprocess
import tempfile

logger = logging.getLogger(__name__)

# OpenAI Whisper API has a 25MB file size limit
MAX_FILE_SIZE = 25 * 1024 * 1024  # 25MB in bytes


def _compress_audio_if_needed(audio_file_path: str) -> str:
    """
    Compress audio file if it exceeds the size limit.
    
    Args:
        audio_file_path: Path to original audio file
        
    Returns:
        Path to compressed audio file (or original if under limit)
    """
    file_size = os.path.getsize(audio_file_path)
    
    if file_size <= MAX_FILE_SIZE:
        logger.info(f"File size ({file_size / 1024 / 1024:.2f}MB) is under limit, using original")
        return audio_file_path
    
    logger.warning(f"File size ({file_size / 1024 / 1024:.2f}MB) exceeds limit, compressing...")
    
    # Create temporary compressed file
    temp_dir = tempfile.gettempdir()
    compressed_path = os.path.join(temp_dir, f"compressed_{os.path.basename(audio_file_path)}")
    
    try:
        # Use ffmpeg to compress to lower bitrate (64kbps should be enough for speech)
        # and ensure it's under 25MB
        subprocess.run([
            'ffmpeg', '-i', audio_file_path,
            '-codec:a', 'libmp3lame',
            '-b:a', '64k',
            '-ar', '16000',  # Sample rate good for speech
            '-y',  # Overwrite output file
            compressed_path
        ], check=True, capture_output=True)
        
        compressed_size = os.path.getsize(compressed_path)
        logger.info(f"Compressed file size: {compressed_size / 1024 / 1024:.2f}MB")
        
        if compressed_size > MAX_FILE_SIZE:
            logger.warning("Compressed file still too large, trying 32kbps")
            # Try even lower bitrate
            subprocess.run([
                'ffmpeg', '-i', audio_file_path,
                '-codec:a', 'libmp3lame',
                '-b:a', '32k',
                '-ar', '16000',
                '-y',
                compressed_path
            ], check=True, capture_output=True)
        
        return compressed_path
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Error compressing audio: {e}")
        raise Exception(f"Failed to compress audio file: {str(e)}")


def transcribe_audio(audio_file_path: str, api_key: Optional[str] = None) -> str:
    """
    Transcribe audio file using OpenAI Whisper API.
    Handles files over 25MB by compressing them first.
    
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
    
    compressed_path = None
    
    try:
        logger.info(f"Starting transcription for file: {audio_file_path}")
        
        # Compress if needed
        audio_to_transcribe = _compress_audio_if_needed(audio_file_path)
        compressed_path = audio_to_transcribe if audio_to_transcribe != audio_file_path else None
        
        # Open the audio file
        with open(audio_to_transcribe, 'rb') as audio_file:
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
    finally:
        # Clean up compressed file if we created one
        if compressed_path and compressed_path != audio_file_path and os.path.exists(compressed_path):
            try:
                os.unlink(compressed_path)
                logger.info(f"Cleaned up compressed file: {compressed_path}")
            except Exception as e:
                logger.warning(f"Failed to clean up compressed file: {str(e)}")

