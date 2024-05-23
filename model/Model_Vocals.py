import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
current_dir = os.path.dirname(os.path.abspath(__file__))
from utils.Audio import PrintAudioInfo, GetAudio, remove_Silence
from utils.levenshtein_distance import infer
from utils.Tokenize_Kor import decompose_tokens
from transformers import Wav2Vec2ForCTC
from transformers import Wav2Vec2Processor
import torch
import numpy as np
import torch.multiprocessing as mp
from transformers import Wav2Vec2Config
from collections import Counter

Vocals_model = None
Vocals_processor = None

def LoadModel():
    global Vocals_model
    global Vocals_processor
    print("LoadModel...")
    if(Vocals_model is None):
        model_config = Wav2Vec2Config.from_json_file(os.path.join(current_dir,'Model','model_config.json'))
        Vocals_model = Wav2Vec2ForCTC(model_config)
        model_dict = torch.load(os.path.join(current_dir,'Model','model_state.pt'))
        Vocals_model.load_state_dict(model_dict)
        Vocals_model.eval()
        Vocals_processor = Wav2Vec2Processor.from_pretrained(os.path.join(current_dir,'Model','processor_config'))
    print("LoadModel...DONE")

def worker(args):
        global Vocals_model
        global Vocals_processor
        num, audio = args
        if(audio == None):
            return None
        print('worker', num, "start")
        input = Vocals_processor(np.array(audio.set_channels(1).get_array_of_samples(), dtype=np.float32), sampling_rate=16000, return_tensors="pt").input_values[0]
        with torch.no_grad():
            input_values = input.unsqueeze(0)
            logits = Vocals_model(input_values).logits
            predlogits = torch.argmax(logits, dim=-1)[0]
            outputs = Vocals_processor.decode(predlogits, output_char_offsets=True)
        print('worker', num, "end")
        return outputs

class Model_Vocals:
    def __init__(self):
        self.poolNum = 1
        self.pool = None
    def initialize(self , num):
        LoadModel()
        if self.pool is not None:
            self.close_pool()
        self.poolNum = num
        self.pool = mp.Pool(processes=self.poolNum, initializer=LoadModel)
    def SaveModel(self):
        model_id = 'hongseongpil/wav2vec2-Vocals-Kor'
        revision = '9804430a50f2feab572a90abbb6c584a7f212118'
        Vocals_model = Wav2Vec2ForCTC.from_pretrained(model_id,revision = revision, output_attentions=True)
        processor = Wav2Vec2Processor.from_pretrained(model_id,revision = revision)
        processor.save_pretrained(os.path.join(current_dir,'Model','processor_config'))
        torch.save(Vocals_model.state_dict(), os.path.join(current_dir,'Model','model_state.pt'))
        Vocals_model.config.to_json_file(os.path.join(current_dir,'Model','model_config.json'))
    
    def __call__(self, audio_path, label):
        audio = GetAudio(audio_path)
        decomposed = decompose_tokens(label)
        while ' ' in decomposed[0]:
            index = decomposed[0].index(' ')
            del decomposed[0][index]
            del decomposed[1][index]
        interval = audio.duration_seconds / self.poolNum
        start_times = [i * interval for i in range(self.poolNum)]
        end_times = [start + interval for start in start_times]
        audio_segments = []
        for start, end in zip(start_times, end_times):
            segment = audio[int(start*1000):int(end*1000)]
            audio_segments.append(segment)
        predtext = ""
        charoffset = []
        time_offset = Vocals_model.config.inputs_to_logits_ratio / Vocals_processor.feature_extractor.sampling_rate
        for i , output in enumerate(self.pool.map(worker, [(i, audio_segments[i]) for i in range(self.poolNum)])):
            predtext += output['text'].replace(' ','')
            for j in range(len(output['char_offsets'])):
                start_offset = output['char_offsets'][j]["start_offset"]
                output['char_offsets'][j]["start_offset"] = round (start_offset* time_offset, 2 ) + start_times[i] 
                end_offset = output['char_offsets'][j]["end_offset"]
                output['char_offsets'][j]["end_offset"] = round (end_offset* time_offset, 2 ) + start_times[i]
            charoffset.extend(output['char_offsets'])
        print("infer .. start")
        origintext = "".join(decomposed[0])
        count_dict = dict(Counter(decomposed[1]))
        count_list = [[num, count] for num, count in count_dict.items()]
        infered = infer(origintext,predtext)
        result = []
        phoneme_index = 0
        end_index = -1
        for i in count_list:
            start_index = infered[phoneme_index][1][0]-1
            start_offset = charoffset[start_index]["start_offset"]
            if result and (result[-1]["end"]>charoffset[start_index]["start_offset"]):
                result[-1]["end"] = charoffset[start_index]["start_offset"]
            end_index = infered[phoneme_index+i[1]-1][1][-1]-1
            phoneme_index += i[1]
            end_offset = charoffset[end_index]["end_offset"]
            result.append({'char' : label[i[0]],'start':start_offset,'end' :end_offset,'pitch':'c4'})
        print("infer .. Done")
        for item in infered:
            pred ="".join([predtext[j-1] for j in item[1]])
            print("origintext:", origintext[item[0]-1],"predtext:",pred)
        return result 

    def close_pool(self):
        if self.pool is not None:
            self.pool.close()
            self.pool.join()
            self.pool = None
            