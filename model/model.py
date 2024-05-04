import sys,os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
current_dir = os.path.dirname(os.path.abspath(__file__))
from utils.Audio import PrintAudioInfo, GetAudio, remove_Silence
from utils.levenshtein_distance import infer
from utils.Tokenize_Kor import decompose_tokens
from transformers import Wav2Vec2ForCTC
from transformers import Wav2Vec2Processor
import torch
import numpy as np
from IPython.display import display
from IPython.display import Audio
from IPython import get_ipython
from collections import Counter

class Model_Vocals:
    def __init__(self):
        model_id = 'hongseongpil/wav2vec2-vocals'
        self.model = Wav2Vec2ForCTC.from_pretrained(model_id,output_attentions=True)
        self.model.eval()
        self.processor = Wav2Vec2Processor.from_pretrained(model_id)
