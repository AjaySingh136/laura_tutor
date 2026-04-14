import logging
from typing import Optional, Tuple
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import requests

logger = logging.getLogger(__name__)

class YouTubeService:
    """Service for handling YouTube video transcription and metadata"""
    
    @staticmethod
    def extract_video_id(url: str) -> Optional[str]:
        """Extract video ID from various YouTube URL formats"""
        try:
            # Handle different URL formats
            if "youtube.com" in url:
                parsed = urlparse(url)
                video_id = parse_qs(parsed.query).get('v', [None])[0]
            elif "youtu.be" in url:
                video_id = url.split('/')[-1].split('?')[0]
            else:
                return None
                
            return video_id
        except Exception as e:
            logger.error(f"Error extracting video ID: {str(e)}")
            return None
    
    @staticmethod
    def get_transcript(url: str) -> Optional[str]:
        """Get transcript from YouTube video"""
        try:
            video_id = YouTubeService.extract_video_id(url)
            if not video_id:
                raise ValueError("Invalid YouTube URL")
            
            # Get available transcripts
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # Get English transcript or first available
            try:
                transcript = transcript_list.find_transcript(['en'])
            except:
                transcript = transcript_list.find_manually_created_transcript(['en'])
            
            # Combine transcript entries
            transcript_text = " ".join([entry['text'] for entry in transcript.fetch()])
            return transcript_text
            
        except Exception as e:
            logger.error(f"Error getting YouTube transcript: {str(e)}")
            return None
    
    @staticmethod
    def get_video_metadata(url: str) -> Optional[dict]:
        """Get video metadata (title, duration, etc.)"""
        try:
            video_id = YouTubeService.extract_video_id(url)
            if not video_id:
                return None
            
            # For now, return basic info
            # In production, use YouTube Data API
            return {
                "video_id": video_id,
                "url": url,
                "title": "YouTube Video"  # Would need YouTube API key for actual title
            }
            
        except Exception as e:
            logger.error(f"Error getting video metadata: {str(e)}")
            return None

    @staticmethod
    def summarize_transcript(transcript: str, max_sentences: int = 5) -> str:
        """Create a brief summary of the transcript"""
        try:
            sentences = transcript.split('.')
            summary = '. '.join(sentences[:max_sentences])
            if not summary.endswith('.'):
                summary += '.'
            return summary
        except Exception as e:
            logger.error(f"Error summarizing transcript: {str(e)}")
            return transcript[:500]
