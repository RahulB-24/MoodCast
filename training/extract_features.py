import numpy as np
import librosa

def extract_librosa_features(path):
    y, sr = librosa.load(path, sr=22050, mono=True)

    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    zcr = librosa.feature.zero_crossing_rate(y)

    def stats(arr):
        return np.hstack([arr.mean(axis=1), arr.std(axis=1)])

    features = np.hstack([
        stats(mfcc),
        stats(chroma),
        stats(centroid),
        stats(zcr)
    ])

    return features
