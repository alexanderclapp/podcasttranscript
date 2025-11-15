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
    
    # Calculate target summary length
    # Target: ~3000 words, or 1/4 of transcript length if transcript is shorter than 3000 words
    transcript_word_count = len(transcript.split())
    
    if transcript_word_count < 3000:
        target_words = max(transcript_word_count // 4, 200)  # At least 200 words
        target_note = f"approximately {target_words} words (1/4 of transcript length)"
    else:
        target_words = 3000
        target_note = "approximately 3000 words"
    
    # Calculate min and max tokens (roughly 1 token ≈ 0.75 words, so ~1.33 tokens per word)
    # Using conservative estimate: words * 1.25 for min, words * 1.5 for max
    min_tokens = max(int(target_words * 1.1), 250)  # At least 250 tokens (roughly 200 words)
    max_tokens = int(target_words * 1.5)  # Allow some buffer above target
    
    logger.info(f"Transcript word count: {transcript_word_count}, Target summary: {target_words} words, Tokens: min={min_tokens}, max={max_tokens}")
    
    # Handle long transcripts by truncating if needed (keep more for longer summaries)
    # For 3000 word summaries, we need more context
    max_transcript_length = 12000  # Increased to allow for longer summaries
    truncated = False
    original_transcript = transcript
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

Title: "X – key points from the episode" (use lowercase "key points" and "episode")

Short executive snapshot: 5–8 bullets capturing the most important themes. Start directly with bullet points, no introductory text.

Sectioned summary using markdown headings (## and ###). Create clear, logical sections such as:

- **Background / Who is [person]?** - Personal and professional background with multiple bullet points covering education, career path, previous roles, and key experiences. Use nested sub-bullets for details.
- **[Company/Project] – model & capital** - Business structure, funding, investors. Include detailed subsections like "Initial model" and "Now" with multiple bullets each. Cover investor types, capital structure, economics.
- **Acquisitions & sector focus** - Specific deals with detailed breakdowns. For each acquisition, include multiple bullets covering what it was, why it mattered, how it fits the strategy. Include subsections for different deals.
- **Market structure & thesis** - Comprehensive market analysis with multiple bullets on competition, positioning, market size, fragmentation. Include specific numbers and metrics.
- **[Sector] economics** - Detailed business model breakdown with subsections (e.g., "construction vs maintenance"). Multiple bullets per subsection covering revenue streams, margins, profitability, unit economics.
- **Integration, management, and seller roles** - In-depth post-acquisition dynamics. Multiple bullets covering seller retention strategies, management structure, cultural integration challenges, new management hires.
- **Deal sourcing** - Comprehensive coverage of how deals are found. Include subsections for different methods (proprietary, intermediated, etc.). Multiple bullets per method with specifics.
- **Labor market & HR challenges** - Detailed workforce considerations. Multiple bullets on talent scarcity, training programs, hiring strategies, skill requirements.
- **Geographic scope** - Current and future markets with multiple bullets on current presence, expansion plans, regional strategies, target markets.
- **Challenges & opportunities** - Substantial section with multiple bullets on key risks, growth areas, strategic considerations.
- **Future direction or open questions** - What's next with detailed bullets on plans, timelines, priorities.
- **Closing & contact** - How to reach them (if mentioned) with contact details and preferences.

**IMPORTANT**: 

- Target length: {target_note}
- Each section should be SUBSTANTIAL with 5-15+ bullet points (often with nested sub-bullets)
- Don't be brief - extract all relevant details, numbers, frameworks, and insights from the conversation
- Think of each section as a comprehensive mini-essay in bullet format
- Use nested bullet points (sub-bullets with proper indentation) extensively to show hierarchy and detail
- Include specific numbers, dates, percentages, and concrete examples wherever mentioned
- The summary should be comprehensive and detailed, reaching the target word count through thorough coverage of all topics

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
        "min_tokens": min_tokens,  # Minimum tokens based on target length
        "max_tokens": max_tokens  # Maximum tokens based on target length (with buffer)
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

