import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'podcast_summaries.db')


def init_db():
    """Initialize the database with required tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            podcast_url TEXT NOT NULL,
            podcast_title TEXT,
            transcript TEXT NOT NULL,
            summary_type_1 TEXT NOT NULL,
            summary_type_2 TEXT,
            metadata TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(podcast_url)
        )
    ''')
    
    conn.commit()
    conn.close()
    logger.info("Database initialized successfully")


def save_summary(
    podcast_url: str,
    transcript: str,
    summary_type_1: str,
    summary_type_2: Optional[str] = None,
    metadata: Optional[Dict] = None,
    podcast_title: Optional[str] = None
) -> int:
    """Save a summary to the database. Returns the summary ID."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Convert metadata dict to JSON string
    metadata_str = None
    if metadata:
        import json
        metadata_str = json.dumps(metadata)
    
    try:
        cursor.execute('''
            INSERT OR REPLACE INTO summaries 
            (podcast_url, podcast_title, transcript, summary_type_1, summary_type_2, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (podcast_url, podcast_title, transcript, summary_type_1, summary_type_2, metadata_str))
        
        summary_id = cursor.lastrowid
        conn.commit()
        logger.info(f"Summary saved with ID: {summary_id}")
        return summary_id
    finally:
        conn.close()


def get_all_summaries(limit: int = 50) -> List[Dict]:
    """Retrieve all summaries, most recent first."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, podcast_url, podcast_title, summary_type_1, summary_type_2, 
               metadata, created_at
        FROM summaries
        ORDER BY created_at DESC
        LIMIT ?
    ''', (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    
    summaries = []
    for row in rows:
        summary = {
            'id': row['id'],
            'podcast_url': row['podcast_url'],
            'podcast_title': row['podcast_title'],
            'summary_type_1': row['summary_type_1'],
            'summary_type_2': row['summary_type_2'],
            'created_at': row['created_at'],
        }
        
        # Parse metadata if it exists
        if row['metadata']:
            import json
            try:
                summary['metadata'] = json.loads(row['metadata'])
            except:
                summary['metadata'] = {}
        else:
            summary['metadata'] = {}
            
        summaries.append(summary)
    
    return summaries


def get_summary_by_id(summary_id: int) -> Optional[Dict]:
    """Retrieve a specific summary by ID."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, podcast_url, podcast_title, transcript, summary_type_1, 
               summary_type_2, metadata, created_at
        FROM summaries
        WHERE id = ?
    ''', (summary_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
    
    summary = {
        'id': row['id'],
        'podcast_url': row['podcast_url'],
        'podcast_title': row['podcast_title'],
        'transcript': row['transcript'],
        'summary_type_1': row['summary_type_1'],
        'summary_type_2': row['summary_type_2'],
        'created_at': row['created_at'],
    }
    
    # Parse metadata
    if row['metadata']:
        import json
        try:
            summary['metadata'] = json.loads(row['metadata'])
        except:
            summary['metadata'] = {}
    else:
        summary['metadata'] = {}
    
    return summary

