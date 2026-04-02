"""
IntervYou Confidence Classifier
Custom ML model that predicts speaker confidence from audio + text features.
Uses scikit-learn Random Forest trained on extracted Librosa features.
"""
import os
import json
import numpy as np
import librosa
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'ml_models')
MODEL_PATH = os.path.join(MODEL_DIR, 'confidence_model.pkl')
SCALER_PATH = os.path.join(MODEL_DIR, 'confidence_scaler.pkl')

_model = None
_scaler = None

# Confidence levels
LABELS = ['low', 'medium', 'high']


def extract_audio_features(audio_path):
    """
    Extract audio features from a recording for confidence prediction.
    Returns a dict of features that indicate speaker confidence.
    """
    try:
        y, sr = librosa.load(audio_path, sr=22050, mono=True)
        duration = librosa.get_duration(y=y, sr=sr)

        if duration < 0.5:
            return _empty_features()

        # 1. Pitch (F0) features — confident speakers have stable, moderate pitch
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_values = []
        for t in range(pitches.shape[1]):
            index = magnitudes[:, t].argmax()
            pitch = pitches[index, t]
            if pitch > 0:
                pitch_values.append(pitch)

        pitch_values = np.array(pitch_values) if pitch_values else np.array([0.0])
        pitch_mean = float(np.mean(pitch_values))
        pitch_std = float(np.std(pitch_values))
        pitch_range = float(np.max(pitch_values) - np.min(pitch_values))

        # 2. Energy/volume features — confident speakers have consistent energy
        rms = librosa.feature.rms(y=y)[0]
        energy_mean = float(np.mean(rms))
        energy_std = float(np.std(rms))
        energy_range = float(np.max(rms) - np.min(rms))

        # 3. Speaking rate and pauses
        intervals = librosa.effects.split(y, top_db=25)
        num_segments = len(intervals)
        pause_count = max(0, num_segments - 1)

        # Calculate pause durations
        pause_durations = []
        for i in range(1, len(intervals)):
            gap_start = intervals[i - 1][1]
            gap_end = intervals[i][0]
            pause_dur = (gap_end - gap_start) / sr
            if pause_dur > 0.1:  # Only count pauses > 100ms
                pause_durations.append(pause_dur)

        avg_pause_duration = float(np.mean(pause_durations)) if pause_durations else 0.0
        max_pause_duration = float(np.max(pause_durations)) if pause_durations else 0.0
        long_pauses = sum(1 for p in pause_durations if p > 1.5)  # Pauses > 1.5s

        # 4. Speech ratio — how much of the recording is actual speech
        speech_frames = sum(end - start for start, end in intervals)
        speech_ratio = float(speech_frames / len(y)) if len(y) > 0 else 0.0

        # 5. Tempo / rhythm regularity
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        tempo = librosa.feature.tempo(onset_envelope=onset_env, sr=sr)[0]

        # 6. Spectral features — voice quality
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        spectral_mean = float(np.mean(spectral_centroid))

        # 7. Zero crossing rate — higher in hesitant/breathy speech
        zcr = librosa.feature.zero_crossing_rate(y)[0]
        zcr_mean = float(np.mean(zcr))

        return {
            'duration': round(duration, 2),
            'pitch_mean': round(pitch_mean, 2),
            'pitch_std': round(pitch_std, 2),
            'pitch_range': round(pitch_range, 2),
            'energy_mean': round(energy_mean, 6),
            'energy_std': round(energy_std, 6),
            'energy_range': round(energy_range, 6),
            'pause_count': pause_count,
            'avg_pause_duration': round(avg_pause_duration, 3),
            'max_pause_duration': round(max_pause_duration, 3),
            'long_pauses': long_pauses,
            'speech_ratio': round(speech_ratio, 3),
            'tempo': round(float(tempo), 2),
            'spectral_mean': round(spectral_mean, 2),
            'zcr_mean': round(zcr_mean, 6),
        }

    except Exception as e:
        print(f'Feature extraction error: {e}')
        return _empty_features()


def extract_text_features(transcript, speaking_rate, filler_count):
    """Extract text-based features that indicate confidence."""
    words = transcript.split() if transcript else []
    word_count = len(words)

    # Hedging words indicate low confidence
    hedging_words = {'maybe', 'perhaps', 'possibly', 'might', 'could',
                     'i think', 'i guess', 'sort of', 'kind of', 'probably',
                     'not sure', 'i believe', 'it seems'}
    text_lower = transcript.lower() if transcript else ''
    hedge_count = sum(1 for h in hedging_words if h in text_lower)

    # Strong/assertive words indicate high confidence
    strong_words = {'definitely', 'certainly', 'absolutely', 'clearly',
                    'specifically', 'achieved', 'led', 'delivered',
                    'managed', 'created', 'improved', 'increased'}
    strong_count = sum(1 for s in strong_words if s in text_lower)

    # Sentence length variety — confident speakers vary their structure
    sentences = [s.strip() for s in text_lower.replace('!', '.').replace('?', '.').split('.') if s.strip()]
    sentence_lengths = [len(s.split()) for s in sentences] if sentences else [0]
    sentence_len_std = float(np.std(sentence_lengths)) if len(sentence_lengths) > 1 else 0.0

    # First person usage — confident speakers own their statements
    first_person = text_lower.count(' i ') + text_lower.count('i ') + text_lower.count(' my ') + text_lower.count(' me ')

    return {
        'word_count': word_count,
        'speaking_rate': round(speaking_rate, 1),
        'filler_count': filler_count,
        'filler_ratio': round(filler_count / max(word_count, 1), 4),
        'hedge_count': hedge_count,
        'strong_count': strong_count,
        'sentence_count': len(sentences),
        'avg_sentence_length': round(float(np.mean(sentence_lengths)), 1) if sentence_lengths else 0,
        'sentence_len_std': round(sentence_len_std, 2),
        'first_person_count': first_person,
    }


def _features_to_vector(audio_feats, text_feats):
    """Convert feature dicts to a numpy vector for the model."""
    return np.array([
        audio_feats.get('pitch_mean', 0),
        audio_feats.get('pitch_std', 0),
        audio_feats.get('pitch_range', 0),
        audio_feats.get('energy_mean', 0),
        audio_feats.get('energy_std', 0),
        audio_feats.get('energy_range', 0),
        audio_feats.get('pause_count', 0),
        audio_feats.get('avg_pause_duration', 0),
        audio_feats.get('max_pause_duration', 0),
        audio_feats.get('long_pauses', 0),
        audio_feats.get('speech_ratio', 0),
        audio_feats.get('tempo', 0),
        audio_feats.get('spectral_mean', 0),
        audio_feats.get('zcr_mean', 0),
        text_feats.get('word_count', 0),
        text_feats.get('speaking_rate', 0),
        text_feats.get('filler_count', 0),
        text_feats.get('filler_ratio', 0),
        text_feats.get('hedge_count', 0),
        text_feats.get('strong_count', 0),
        text_feats.get('sentence_count', 0),
        text_feats.get('avg_sentence_length', 0),
        text_feats.get('sentence_len_std', 0),
        text_feats.get('first_person_count', 0),
    ]).reshape(1, -1)


def _empty_features():
    return {k: 0 for k in [
        'duration', 'pitch_mean', 'pitch_std', 'pitch_range',
        'energy_mean', 'energy_std', 'energy_range',
        'pause_count', 'avg_pause_duration', 'max_pause_duration', 'long_pauses',
        'speech_ratio', 'tempo', 'spectral_mean', 'zcr_mean'
    ]}


def predict_confidence(audio_path=None, transcript='', speaking_rate=0, filler_count=0):
    """
    Predict confidence level from audio and text features.
    Returns: { level: 'low'|'medium'|'high', score: 0-100, features: {...} }
    """
    global _model, _scaler

    # Extract features
    if audio_path and os.path.exists(audio_path):
        audio_feats = extract_audio_features(audio_path)
    else:
        audio_feats = _empty_features()

    text_feats = extract_text_features(transcript, speaking_rate, filler_count)
    vector = _features_to_vector(audio_feats, text_feats)

    # Try to load trained model
    if _model is None and os.path.exists(MODEL_PATH):
        try:
            _model = joblib.load(MODEL_PATH)
            _scaler = joblib.load(SCALER_PATH)
            print('Loaded trained confidence model')
        except Exception as e:
            print(f'Could not load model: {e}')

    # If model exists, use it
    if _model is not None and _scaler is not None:
        try:
            scaled = _scaler.transform(vector)
            prediction = _model.predict(scaled)[0]
            probabilities = _model.predict_proba(scaled)[0]
            confidence_score = round(float(probabilities[prediction]) * 100, 1)
            level = LABELS[prediction]
        except Exception as e:
            print(f'Prediction error: {e}')
            level, confidence_score = _rule_based_confidence(audio_feats, text_feats)
    else:
        # Fallback: rule-based confidence estimation
        level, confidence_score = _rule_based_confidence(audio_feats, text_feats)

    return {
        'level': level,
        'score': confidence_score,
        'audio_features': audio_feats,
        'text_features': text_feats
    }


def _rule_based_confidence(audio_feats, text_feats):
    """Rule-based fallback when no trained model is available."""
    score = 50.0  # Start neutral

    # Speaking rate: 120-160 wpm is confident
    rate = text_feats.get('speaking_rate', 0)
    if 120 <= rate <= 160:
        score += 10
    elif rate < 80 or rate > 200:
        score -= 15
    elif rate < 100 or rate > 180:
        score -= 5

    # Filler words: fewer is more confident
    filler_ratio = text_feats.get('filler_ratio', 0)
    if filler_ratio < 0.02:
        score += 10
    elif filler_ratio > 0.08:
        score -= 15
    elif filler_ratio > 0.05:
        score -= 8

    # Hedging vs strong words
    score -= text_feats.get('hedge_count', 0) * 5
    score += text_feats.get('strong_count', 0) * 4

    # Word count: too short = low confidence
    wc = text_feats.get('word_count', 0)
    if wc < 20:
        score -= 15
    elif wc > 50:
        score += 5

    # Pauses
    if audio_feats.get('long_pauses', 0) > 3:
        score -= 10
    if audio_feats.get('speech_ratio', 0) > 0.7:
        score += 8
    elif audio_feats.get('speech_ratio', 0) < 0.4:
        score -= 10

    # Energy consistency
    if audio_feats.get('energy_std', 0) > 0 and audio_feats.get('energy_mean', 0) > 0:
        cv = audio_feats['energy_std'] / audio_feats['energy_mean']
        if cv < 0.5:
            score += 5  # Consistent energy = confident
        elif cv > 1.5:
            score -= 5  # Erratic energy = nervous

    score = max(0, min(100, score))

    if score >= 65:
        level = 'high'
    elif score >= 40:
        level = 'medium'
    else:
        level = 'low'

    return level, round(score, 1)
