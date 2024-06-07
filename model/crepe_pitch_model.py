import crepe
import librosa
import numpy as np

# 음계 이름과 MIDI 번호 매핑
MIDI_TO_NOTE = {
    60: 'C4', 61: 'C#4', 62: 'D4', 63: 'D#4', 64: 'E4', 65: 'F4', 66: 'F#4', 67: 'G4', 68: 'G#4', 69: 'A4', 70: 'A#4', 71: 'B4',
    72: 'C5', 73: 'C#5', 74: 'D5', 75: 'D#5', 76: 'E5', 77: 'F5', 78: 'F#5', 79: 'G5', 80: 'G#5', 81: 'A5', 82: 'A#5', 83: 'B5'
}

def extract_pitch_crepe(wav_file, step_size=10, model_capacity='full'):
    """
    CREPE 모델을 사용하여 WAV 파일에서 피치를 추출합니다.

    :param wav_file: 분석할 WAV 파일 경로
    :param step_size: CREPE 모델의 스텝 크기
    :param model_capacity: CREPE 모델 용량 ('tiny', 'small', 'medium', 'large', 'full')
    :return: time, frequency, confidence
    """
    y, sr = librosa.load(wav_file, sr=16000)  # CREPE는 16kHz 샘플링을 사용
    time, frequency, confidence, activation = crepe.predict(y, sr, step_size=step_size, model_capacity=model_capacity)
    return time, frequency, confidence
