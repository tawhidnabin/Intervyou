"""
Train the IntervYou Confidence Classifier.

This script generates synthetic training data based on known patterns
of confident vs unconfident speech, then trains a Random Forest model.

In production, replace synthetic data with real labelled recordings.
Run: python train_confidence_model.py
"""
import os
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score

MODEL_DIR = os.path.join(os.path.dirname(__file__), 'ml_models')
os.makedirs(MODEL_DIR, exist_ok=True)

np.random.seed(42)

FEATURE_NAMES = [
    'pitch_mean', 'pitch_std', 'pitch_range',
    'energy_mean', 'energy_std', 'energy_range',
    'pause_count', 'avg_pause_duration', 'max_pause_duration', 'long_pauses',
    'speech_ratio', 'tempo', 'spectral_mean', 'zcr_mean',
    'word_count', 'speaking_rate', 'filler_count', 'filler_ratio',
    'hedge_count', 'strong_count', 'sentence_count',
    'avg_sentence_length', 'sentence_len_std', 'first_person_count',
]

# Labels: 0=low, 1=medium, 2=high
N_SAMPLES = 300  # 100 per class


def generate_synthetic_data():
    """
    Generate training data based on research on confident speech patterns:
    - Confident: steady pitch, consistent energy, few pauses, 120-160 wpm, few fillers
    - Medium: moderate variation, some pauses, 100-170 wpm, some fillers
    - Low: high pitch variation, inconsistent energy, many pauses, <100 or >180 wpm, many fillers
    """
    X = []
    y = []

    for _ in range(N_SAMPLES // 3):
        # HIGH confidence
        X.append([
            np.random.uniform(150, 250),    # pitch_mean (moderate, steady)
            np.random.uniform(10, 30),      # pitch_std (low variation)
            np.random.uniform(30, 80),      # pitch_range (narrow)
            np.random.uniform(0.03, 0.08),  # energy_mean (strong)
            np.random.uniform(0.005, 0.015),# energy_std (consistent)
            np.random.uniform(0.02, 0.05),  # energy_range
            np.random.randint(1, 5),        # pause_count (few)
            np.random.uniform(0.2, 0.5),    # avg_pause_duration (short)
            np.random.uniform(0.3, 0.8),    # max_pause_duration
            0,                              # long_pauses (none)
            np.random.uniform(0.7, 0.9),    # speech_ratio (high)
            np.random.uniform(100, 140),    # tempo (steady)
            np.random.uniform(1500, 2500),  # spectral_mean
            np.random.uniform(0.03, 0.06),  # zcr_mean
            np.random.randint(60, 150),     # word_count (substantial)
            np.random.uniform(120, 160),    # speaking_rate (optimal)
            np.random.randint(0, 3),        # filler_count (very few)
            np.random.uniform(0, 0.03),     # filler_ratio
            np.random.randint(0, 1),        # hedge_count (none/minimal)
            np.random.randint(2, 6),        # strong_count (several)
            np.random.randint(3, 8),        # sentence_count
            np.random.uniform(10, 20),      # avg_sentence_length
            np.random.uniform(3, 8),        # sentence_len_std (varied)
            np.random.randint(3, 8),        # first_person_count
        ])
        y.append(2)  # high

        # MEDIUM confidence
        X.append([
            np.random.uniform(130, 280),    # pitch_mean
            np.random.uniform(25, 50),      # pitch_std (moderate)
            np.random.uniform(60, 150),     # pitch_range
            np.random.uniform(0.02, 0.06),  # energy_mean
            np.random.uniform(0.01, 0.025), # energy_std
            np.random.uniform(0.03, 0.07),  # energy_range
            np.random.randint(3, 10),       # pause_count
            np.random.uniform(0.4, 0.9),    # avg_pause_duration
            np.random.uniform(0.8, 1.8),    # max_pause_duration
            np.random.randint(0, 2),        # long_pauses
            np.random.uniform(0.5, 0.75),   # speech_ratio
            np.random.uniform(80, 130),     # tempo
            np.random.uniform(1200, 2200),  # spectral_mean
            np.random.uniform(0.04, 0.08),  # zcr_mean
            np.random.randint(30, 80),      # word_count
            np.random.uniform(100, 170),    # speaking_rate
            np.random.randint(3, 8),        # filler_count
            np.random.uniform(0.03, 0.08),  # filler_ratio
            np.random.randint(1, 4),        # hedge_count
            np.random.randint(0, 3),        # strong_count
            np.random.randint(2, 6),        # sentence_count
            np.random.uniform(8, 16),       # avg_sentence_length
            np.random.uniform(2, 6),        # sentence_len_std
            np.random.randint(1, 5),        # first_person_count
        ])
        y.append(1)  # medium

        # LOW confidence
        X.append([
            np.random.uniform(100, 320),    # pitch_mean (erratic)
            np.random.uniform(40, 80),      # pitch_std (high variation)
            np.random.uniform(120, 250),    # pitch_range (wide)
            np.random.uniform(0.01, 0.04),  # energy_mean (weak)
            np.random.uniform(0.02, 0.04),  # energy_std (inconsistent)
            np.random.uniform(0.05, 0.1),   # energy_range
            np.random.randint(8, 20),       # pause_count (many)
            np.random.uniform(0.8, 2.0),    # avg_pause_duration (long)
            np.random.uniform(1.5, 4.0),    # max_pause_duration
            np.random.randint(2, 8),        # long_pauses (several)
            np.random.uniform(0.25, 0.55),  # speech_ratio (low)
            np.random.uniform(60, 100),     # tempo (slow/irregular)
            np.random.uniform(800, 1800),   # spectral_mean
            np.random.uniform(0.06, 0.12),  # zcr_mean (breathy)
            np.random.randint(10, 40),      # word_count (short answers)
            np.random.uniform(60, 110),     # speaking_rate (slow)
            np.random.randint(6, 15),       # filler_count (many)
            np.random.uniform(0.08, 0.2),   # filler_ratio
            np.random.randint(3, 8),        # hedge_count (many)
            np.random.randint(0, 1),        # strong_count (none)
            np.random.randint(1, 4),        # sentence_count (few)
            np.random.uniform(5, 12),       # avg_sentence_length (short)
            np.random.uniform(1, 4),        # sentence_len_std
            np.random.randint(0, 3),        # first_person_count
        ])
        y.append(0)  # low

    return np.array(X), np.array(y)


def train():
    print('Generating synthetic training data...')
    X, y = generate_synthetic_data()
    print(f'Dataset: {X.shape[0]} samples, {X.shape[1]} features')
    print(f'Class distribution: low={sum(y==0)}, medium={sum(y==1)}, high={sum(y==2)}')

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train Random Forest
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        random_state=42,
        class_weight='balanced'
    )

    # Cross-validation
    scores = cross_val_score(model, X_scaled, y, cv=5, scoring='accuracy')
    print(f'Cross-validation accuracy: {scores.mean():.3f} (+/- {scores.std():.3f})')

    # Train on full dataset
    model.fit(X_scaled, y)

    # Feature importance
    print('\nTop 10 most important features:')
    importances = sorted(zip(FEATURE_NAMES, model.feature_importances_), key=lambda x: -x[1])
    for name, imp in importances[:10]:
        print(f'  {name}: {imp:.4f}')

    # Save model
    joblib.dump(model, os.path.join(MODEL_DIR, 'confidence_model.pkl'))
    joblib.dump(scaler, os.path.join(MODEL_DIR, 'confidence_scaler.pkl'))
    print(f'\nModel saved to {MODEL_DIR}/')
    print('Done!')


if __name__ == '__main__':
    train()
