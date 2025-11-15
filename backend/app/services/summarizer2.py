import os
import requests
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def summarize_transcript_type2(transcript: str, api_key: Optional[str] = None) -> str:
    """
    Generate structured summary (Type 2) of transcript using OpenRouter API.
    Focuses on facts, frameworks, numbers, and structured format.
    
    Args:
        transcript: Full transcript text
        api_key: OpenRouter API key (optional, can use env var)
        
    Returns:
        Structured summary text
    """
    api_key = api_key or os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        raise ValueError("OpenRouter API key is required")
    
    # OpenRouter API endpoint
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/alexanderclapp/podcast-transcription",
        "X-Title": "Podcast Transcription App"
    }
    
    # Handle long transcripts by truncating if needed
    max_transcript_length = 8000
    truncated = False
    if len(transcript) > max_transcript_length:
        logger.warning(f"Transcript is very long ({len(transcript)} chars), truncating for summary")
        transcript = transcript[:max_transcript_length] + "... [truncated]"
        truncated = True
    
    transcript_note = " (note: transcript has been truncated)" if truncated else ""
    
    prompt = f"""You are a specialist summariser for long-form content: podcasts, interviews, fireside chats, and multi-hour transcripts.

Your job is to turn long transcripts into clear, structured, highly readable summaries that preserve all key insights, arguments, frameworks, decisions, numbers, and chronology.

**STYLE & TONE**

Write in clean, concise English.

Avoid fluff, filler, introductions ("welcome to the show"), and small talk.

Follow the structure of the conversation, but reorganize where necessary for clarity.

Use headings (###) and bullet points.

Prefer facts, actionable insights, frameworks, and takeaways over storytelling.

**OUTPUT FORMAT**

Title: "X – Key Points from the Conversation"

Short executive snapshot: 5–8 bullets capturing the most important themes.

Sectioned summary, usually (adapt where needed):

- Who the guest is / background

- Their company / project / work

- Key topics discussed

- Frameworks, lessons, or principles

- Data + numbers (revenue, years, metrics, costs, etc.)

- Challenges & opportunities

- Future direction or open questions

Final section: "Why this conversation matters" or "Key takeaways"

**RULES**

Do not repeat or rephrase the entire transcript.

Do not add opinions or analysis not grounded in the transcript.

Extract and retain all important numbers, timelines, strategies, and structures.

If the conversation contains tangents, reorganize them into coherent sections.

Ignore podcast housekeeping ("follow us on Apple", etc.) unless relevant.

**Transcript{transcript_note}:**

{transcript}

**Summary:**"""
    
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 2000  # Structured summaries with sections
    }
    
    try:
        logger.info("Generating Type 2 structured summary using OpenRouter API")
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        summary = result["choices"][0]["message"]["content"]
        
        logger.info("Type 2 summary generated successfully")
        return summary
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling OpenRouter API: {str(e)}")
        raise Exception(f"Failed to generate summary: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error during summarization: {str(e)}")
        raise Exception(f"Failed to generate summary: {str(e)}")

