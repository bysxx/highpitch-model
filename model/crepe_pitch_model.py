
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
current_dir = os.path.dirname(os.path.abspath(__file__))

import crepe
import librosa
from pydub import AudioSegment
import numpy as np

# 음계 이름과 MIDI 번호 매핑
MIDI_TO_NOTE = {
    40: 'E3', 41: 'F3', 42: 'F#3', 43: 'G3', 44: 'G#3', 45: 'A3', 46: 'A#3', 47: 'B3', 48: 'C4', 49: 'C#4', 
    50: 'D3', 51: 'D#3', 52: 'E3', 53: 'F3', 54: 'F#3', 55: 'G3', 56: 'G#3', 57: 'A3', 58: 'A#3', 59: 'B3',
    60: 'C4', 61: 'C#4', 62: 'D4', 63: 'D#4', 64: 'E4', 65: 'F4', 66: 'F#4', 67: 'G4', 68: 'G#4', 69: 'A4', 
    70: 'A#4', 71: 'B4', 72: 'C5', 73: 'C#5', 74: 'D5', 75: 'D#5', 76: 'E5', 77: 'F5', 78: 'F#5', 79: 'G5', 
    80: 'G#5', 81: 'A5', 82: 'A#5', 83: 'B5'
}

def extract_pitch_crepe(audio : AudioSegment , step_size=10, model_capacity='tiny'):
    """
    :param wav_file: 분석할 WAV 파일 경로
    :param step_size: CREPE 모델의 스텝 크기
    :param model_capacity: CREPE 모델 용량 ('tiny', 'small', 'medium', 'large', 'full')
    :return: time, frequency, confidence
    """
    time, frequency, confidence, activation = crepe.predict(np.array(audio.get_array_of_samples()), 16000, step_size=step_size, model_capacity=model_capacity)
    # 이상치에 덜 민감한 평균(mean)을 사용하여 계산하는 코드
    trimmed_mean = frequency
    print(frequency)
    lower_bound = librosa.midi_to_hz(50)
    upper_bound = librosa.midi_to_hz(70)
    valid_indices = (frequency >= lower_bound) & (frequency <= upper_bound)
    if np.any(valid_indices):
        trimmed_frequency = frequency[valid_indices]
        trimmed_mean = np.mean(trimmed_frequency)
    else:
        trimmed_mean = librosa.midi_to_hz(60)
    
    return time, trimmed_mean, confidence

def check_pitch_and_return(audio : AudioSegment):
    """
    :param wav_file: 분석할 WAV 파일 경로
    :param label: 각 피치에 대한 추가 정보가 포함된 단일 라벨 값
    :return: JSON 형식의 피치 추출 결과
    """
    time, frequency, confidence = extract_pitch_crepe(audio)
    # 주파수를 MIDI 번호로 변환
    midi_numbers = librosa.hz_to_midi(frequency).round()
    print(frequency,MIDI_TO_NOTE[midi_numbers])
    return MIDI_TO_NOTE[midi_numbers]
    result = []
    for i, midi in enumerate(midi_numbers):
        if midi in MIDI_TO_NOTE:
            start_offset = time[i]
            end_offset = time[i + 1] if i + 1 < len(time) else time[i] + (time[i] - time[i - 1])
            result.append({
                'char': label,
                'pitch': MIDI_TO_NOTE[midi]
            })
    
    return result

