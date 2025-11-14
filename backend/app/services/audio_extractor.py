import os
import tempfile
import yt_dlp
from typing import Tuple
import logging

logger = logging.getLogger(__name__)


def extract_audio_from_podcast(url: str) -> Tuple[str, dict]:
    """
    Extract audio from Apple Podcasts URL using yt-dlp.
    
    Args:
        url: Apple Podcasts episode URL
        
    Returns:
        Tuple of (audio_file_path, metadata_dict)
    """
    # Create temporary file for audio (without extension - yt-dlp will add it)
    temp_dir = tempfile.gettempdir()
    temp_audio = tempfile.NamedTemporaryFile(
        suffix='',
        delete=False,
        dir=temp_dir,
        prefix='podcast_'
    )
    temp_audio.close()
    
    # yt-dlp will add .mp3 extension after processing
    output_path = temp_audio.name + '.mp3'
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': temp_audio.name + '.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
        'no_warnings': False,
    }
    
    metadata = {}
    
    try:
        logger.info(f"Extracting audio from URL: {url}")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract info
            info = ydl.extract_info(url, download=True)
            
            # Get metadata
            metadata = {
                'title': info.get('title', 'Unknown'),
                'duration': info.get('duration', 0),
                'uploader': info.get('uploader', 'Unknown'),
                'description': info.get('description', ''),
            }
            
            logger.info(f"Successfully extracted audio. Title: {metadata.get('title')}")
            
        return output_path, metadata
        
    except Exception as e:
        # Clean up on error
        if os.path.exists(temp_audio.name):
            try:
                os.unlink(temp_audio.name)
            except:
                pass
        if os.path.exists(output_path):
            try:
                os.unlink(output_path)
            except:
                pass
        logger.error(f"Error extracting audio: {str(e)}")
        raise Exception(f"Failed to extract audio from URL: {str(e)}")

