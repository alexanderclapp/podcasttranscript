import os
from fastapi import APIRouter, HTTPException
from app.models.schemas import PodcastRequest, PodcastResponse
from app.services.audio_extractor import extract_audio_from_podcast
from app.services.transcriber import transcribe_audio
from app.services.summarizer import summarize_transcript
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/process-podcast", response_model=PodcastResponse)
async def process_podcast(request: PodcastRequest):
    """
    Main endpoint to process a podcast:
    1. Extract audio from URL
    2. Transcribe audio
    3. Generate summary
    
    Returns transcript and summary.
    """
    audio_file_path = None
    metadata = {}
    
    try:
        # Get API keys from environment
        openai_api_key = os.getenv("OPENAI_API_KEY")
        openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        
        if not openai_api_key:
            raise HTTPException(
                status_code=500,
                detail="OPENAI_API_KEY environment variable not set"
            )
        
        if not openrouter_api_key:
            raise HTTPException(
                status_code=500,
                detail="OPENROUTER_API_KEY environment variable not set"
            )
        
        podcast_url = str(request.url)
        
        print(f"\n{'='*60}")
        print(f"Processing podcast: {podcast_url}")
        print(f"{'='*60}\n")
        
        # Step 1: Extract audio
        print("Step 1/3: Extracting audio from podcast URL...")
        audio_file_path, metadata = extract_audio_from_podcast(podcast_url)
        print(f"✓ Audio extracted successfully")
        print(f"  Title: {metadata.get('title', 'Unknown')}")
        print(f"  Duration: {metadata.get('duration', 0)} seconds\n")
        
        # Step 2: Transcribe
        print("Step 2/3: Transcribing audio (this may take a while)...")
        transcript = transcribe_audio(audio_file_path, openai_api_key)
        print(f"✓ Transcription completed")
        print(f"  Transcript length: {len(transcript)} characters\n")
        
        # Step 3: Summarize
        print("Step 3/3: Generating summary...")
        summary = summarize_transcript(transcript, openrouter_api_key)
        print(f"✓ Summary generated")
        print(f"  Summary length: {len(summary)} characters\n")
        print(f"{'='*60}")
        print("Processing complete!")
        print(f"{'='*60}\n")
        
        return PodcastResponse(
            transcript=transcript,
            summary=summary,
            metadata=metadata
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing podcast: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing podcast: {str(e)}"
        )
    finally:
        # Clean up audio file
        if audio_file_path and os.path.exists(audio_file_path):
            try:
                os.unlink(audio_file_path)
                logger.info(f"Cleaned up temporary audio file: {audio_file_path}")
            except Exception as e:
                logger.warning(f"Failed to clean up audio file: {str(e)}")

