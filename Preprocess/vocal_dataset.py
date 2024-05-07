import json
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
current_dir = os.path.dirname(os.path.abspath(__file__))
from utils.Audio import GetAudio , remove_Silence

"""
다음색 가이드보컬 데이터 [https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=473] 중
10대 데이터의 폴더구조를 다음과 같의 정의합니다.

```bash
├── train
│   ├── train.txt
│   ├── audiofiles
├── test
    ├── test.txt
    ├── audiofiles
``` 

normalized / 16000 hz / 16 bit / .wav / Maxlength 10 sec

"""

def GenFolder(foldpath):
    if not os.path.exists(foldpath):
        os.makedirs(foldpath)

def read_json(filename):
    with open(filename, "r", encoding='UTF8') as f:
        json_data = json.load(f)
    return json_data

def process_audio_segments(data, audio,filename, type, result_file):
    start_time = -1
    end_time = -1
    lyrics_segments = []
    uuid = 0
    for note in data['notes']:
        length  = end_time - start_time
        if(start_time == -1):
            start_time = float(note['start_time'])
            end_time = float(note['end_time'])
        elif(length < 10):
            end_time = float(note['end_time'])
        elif((float(note['start_time']) > end_time) and len(lyrics_segments)):
            newaudio = audio[int(start_time*1000):int(end_time*1000)]
            newaudio = remove_Silence(newaudio)
            filename_wav = f"{filename}{uuid}.wav"
            newaudio.export(os.path.join(current_dir,'vocal_dataset',f"{type}","audiofiles",filename_wav), format="wav")
            text = f"{filename_wav} {''.join(lyrics_segments)}\n"
            try:
                result_file.write(text)
            except:
                print("에러",text)
            start_time = float(note['start_time']) 
            end_time = float(note['start_time'])
            lyrics_segments = []
            uuid +=1
        lyrics_segments.extend(note['lyric']+" ")

def proc_in_subfolders(folder_path,type,result_file):
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            # 하위 폴더인 경우 재귀적으로 함수 호출
            proc_in_subfolders(item_path,type,result_file)
        elif os.path.isfile(item_path):
            data = read_json(item_path)
            filepath = None
            if(type == 'train'):
                filepath = item_path.replace(os.path.join("1.Training","TL1"),os.path.join("1.Training","TS1"))
            else:
                filepath = item_path.replace(os.path.join("2.Validation","VL1"),os.path.join("2.Validation","VS1"))
            try:
                audio = GetAudio(filepath.replace(".json", ".wav"))
                process_audio_segments(data,audio,item.replace(".json", ""),type,result_file)
            except:
                print("error :",filepath)
if __name__ == "__main__":

    new_data_path = os.path.join(current_dir,"vocal_dataset")
    GenFolder(new_data_path)
    GenFolder(os.path.join(new_data_path,"train"))
    GenFolder(os.path.join(new_data_path,"train","audiofiles"))
    GenFolder(os.path.join(new_data_path,"test"))
    GenFolder(os.path.join(new_data_path,"test","audiofiles"))
    ## Trainset
    with open(os.path.join(current_dir,"vocal_dataset","train","train.txt"), 'w', encoding='UTF8') as result_file:
        proc_in_subfolders(os.path.join(current_dir,'dataset',"1.Training","TL1"),"train",result_file)
    with open(os.path.join(current_dir,"vocal_dataset","test","test.txt"), 'w', encoding='UTF8') as result_file:
        proc_in_subfolders(os.path.join(current_dir,'dataset',"2.Validation","VL1"),"test",result_file)


        