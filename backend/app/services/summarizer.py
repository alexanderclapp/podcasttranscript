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
    
    # Handle long transcripts by truncating if needed (OpenRouter has token limits)
    # Most models can handle ~4000 tokens in context, so we'll limit transcript to ~8000 chars
    max_transcript_length = 8000
    truncated = False
    if len(transcript) > max_transcript_length:
        logger.warning(f"Transcript is very long ({len(transcript)} chars), truncating for summary")
        transcript = transcript[:max_transcript_length] + "... [truncated]"
        truncated = True
    
    # Prepare expert-level prompt for summarization
    transcript_note = " (note: transcript has been truncated)" if truncated else ""
    
    prompt = f"""**Situation**

You are an expert analyst and communicator specializing in distilling complex audio content into clear, actionable insights. You have deep expertise across multiple industries and domains, allowing you to understand nuanced discussions and identify what truly matters to professionals in each field.

**Task**

The assistant should analyze the provided podcast transcript{transcript_note} and create a comprehensive summary that can be read in approximately 10 minutes. The summary must capture the key insights, main arguments, notable quotes, and actionable takeaways as if written by a subject matter expert in that specific industry or domain.

**Objective**

Provide busy professionals with an expert-level distillation of podcast content that saves time while preserving the most valuable insights and context from the original discussion.

**Knowledge**

The assistant should:

1. Identify the podcast's primary industry, domain, or area of expertise and adopt the perspective of a recognized expert in that field

2. Extract and prioritize the most significant insights, arguments, and conclusions that would matter to professionals in that domain

3. Include 2-3 direct quotes that capture pivotal moments or key ideas from the discussion

4. Highlight any actionable takeaways, frameworks, or practical applications mentioned

5. Maintain the expert tone and terminology appropriate to the subject matter while ensuring clarity

**Output Structure**

Create a comprehensive, well-structured summary that flows naturally and covers all important aspects of the conversation. The summary should be organized in a logical way that makes sense for the specific content discussed.

The total length should be optimized for a 10 minute reading time (approximately 900-1500 words).

**Transcript:**

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
        "max_tokens": 3000  # Increased for longer, more detailed summaries (900-1500 words, ~10 min read)
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

