import os
from fastapi import APIRouter, HTTPException
from app.models.schemas import PodcastRequest, PodcastResponse, SummariesListResponse
from app.services.audio_extractor import extract_audio_from_podcast
from app.services.transcriber import transcribe_audio
from app.services.summarizer import summarize_transcript
from app.services.summarizer2 import summarize_transcript_type2
from app.database import init_db, save_summary, get_all_summaries, get_summary_by_id
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize database on module load
init_db()


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
        
        # Step 3: Generate Type 1 summary (expert-level)
        print("Step 3/5: Generating Type 1 summary (expert-level)...")
        summary_type_1 = summarize_transcript(transcript, openrouter_api_key)
        print(f"✓ Type 1 summary generated")
        print(f"  Summary length: {len(summary_type_1)} characters\n")
        
        # Step 4: Generate Type 2 summary (structured)
        print("Step 4/5: Generating Type 2 summary (structured)...")
        summary_type_2 = summarize_transcript_type2(transcript, openrouter_api_key)
        print(f"✓ Type 2 summary generated")
        print(f"  Summary length: {len(summary_type_2)} characters\n")
        
        # Step 5: Save to database
        print("Step 5/5: Saving to database...")
        summary_id = save_summary(
            podcast_url=podcast_url,
            transcript=transcript,
            summary_type_1=summary_type_1,
            summary_type_2=summary_type_2,
            metadata=metadata,
            podcast_title=metadata.get('title', 'Unknown')
        )
        print(f"✓ Saved to database (ID: {summary_id})\n")
        print(f"{'='*60}")
        print("Processing complete!")
        print(f"{'='*60}\n")
        
        return PodcastResponse(
            transcript=transcript,
            summary=summary_type_1,
            summary_type_2=summary_type_2,
            metadata=metadata,
            summary_id=summary_id
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


@router.get("/summaries", response_model=SummariesListResponse)
async def get_summaries():
    """
    Get all saved summaries, most recent first.
    """
    try:
        summaries = get_all_summaries(limit=100)
        return SummariesListResponse(summaries=summaries)
    except Exception as e:
        logger.error(f"Error retrieving summaries: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving summaries: {str(e)}"
        )


@router.get("/summaries/{summary_id}", response_model=PodcastResponse)
async def get_summary(summary_id: int):
    """
    Get a specific summary by ID.
    """
    try:
        summary = get_summary_by_id(summary_id)
        if not summary:
            raise HTTPException(status_code=404, detail="Summary not found")
        
        return PodcastResponse(
            transcript=summary['transcript'],
            summary=summary['summary_type_1'],
            summary_type_2=summary.get('summary_type_2'),
            metadata=summary.get('metadata', {}),
            summary_id=summary['id']
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving summary: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving summary: {str(e)}"
        )

