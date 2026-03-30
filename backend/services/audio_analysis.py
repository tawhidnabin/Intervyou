import librosa
import numpy as np


def analyze_audio(audio_path):
    """Analyse audio file for duration and pause count."""
    try:
        y, sr = librosa.load(audio_path, sr=None, mono=True)
        duration_seconds = librosa.get_duration(y=y, sr=sr)

        # Detect non-silent intervals; gaps between them are pauses
        intervals = librosa.effects.split(y, top_db=25)
        pause_count = max(0, len(intervals) - 1)

        return {
            'duration_seconds': round(duration_seconds, 2),
            'pause_count': int(pause_count)
        }
    except Exception as e:
        print(f'Audio analysis error: {e}')
        return {'duration_seconds': 0.0, 'pause_count': 0}


def analyze_transcript(transcript, duration_seconds):
    """Analyse transcript for speaking rate and filler words."""
    FILLER_WORDS = {
        'um', 'uh', 'er', 'ah', 'like', 'you know', 'basically',
        'literally', 'kind of', 'sort of'
    }

    words = transcript.lower().split()
    word_count = len(words)
    duration_minutes = max(duration_seconds / 60, 0.01)
    speaking_rate = round(word_count / duration_minutes, 1)

    # Count filler words (single and multi-word)
    text_lower = transcript.lower()
    filler_count = 0
    for filler in FILLER_WORDS:
        filler_count += text_lower.count(filler)

    filler_ratio = filler_count / max(word_count, 1)
    rate_penalty = abs(speaking_rate - 130) / 130
    fluency_score = round(max(0.0, min(1.0, 1.0 - filler_ratio * 2 - rate_penalty * 0.5)), 3)

    return {
        'word_count': word_count,
        'speaking_rate': speaking_rate,
        'filler_count': int(filler_count),
        'fluency_score': fluency_score
    }
