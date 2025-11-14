import os
import requests
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def summarize_transcript(transcript: str, api_key: Optional[str] = None) -> str:
    """
    Generate summary of transcript using OpenRouter API (ChatGPT).
    
    Args:
        transcript: Full transcript text
        api_key: OpenRouter API key (optional, can use env var)
        
    Returns:
        Summary text
    """
    api_key = api_key or os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        raise ValueError("OpenRouter API key is required")
    
    # OpenRouter API endpoint
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/alexanderclapp/podcast-transcription",  # Optional
        "X-Title": "Podcast Transcription App"  # Optional
    }
    
    # Prepare prompt for summarization
    prompt = f"""Please provide a comprehensive summary of the following podcast transcript. 
Focus on the main topics, key insights, and important points discussed. 
Keep the summary concise but informative (approximately 3-5 paragraphs).

Transcript:
{transcript}

Summary:"""
    
    # Handle long transcripts by truncating if needed (OpenRouter has token limits)
    # Most models can handle ~4000 tokens in context, so we'll limit transcript to ~8000 chars
    max_transcript_length = 8000
    if len(transcript) > max_transcript_length:
        logger.warning(f"Transcript is very long ({len(transcript)} chars), truncating for summary")
        transcript = transcript[:max_transcript_length] + "... [truncated]"
        prompt = f"""Please provide a comprehensive summary of the following podcast transcript (note: transcript has been truncated).
Focus on the main topics, key insights, and important points discussed. 
Keep the summary concise but informative (approximately 3-5 paragraphs).

Transcript:
{transcript}

Summary:"""
    
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    try:
        logger.info("Generating summary using OpenRouter API")
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        summary = result["choices"][0]["message"]["content"]
        
        logger.info("Summary generated successfully")
        return summary
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling OpenRouter API: {str(e)}")
        raise Exception(f"Failed to generate summary: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error during summarization: {str(e)}")
        raise Exception(f"Failed to generate summary: {str(e)}")

