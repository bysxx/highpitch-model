import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
current_dir = os.path.dirname(os.path.abspath(__file__))
from utils.Audio import remove_Silence , GetAudio

"""
Zeroth Data set[https://www.openslr.org/40/] 폴더구조를 다음과 같의 정의합니다.

```bash
├── train
│   ├── train.txt
│   ├── audiofiles
├── test
    ├── test.txt
    ├── audiofiles
``` 

normalized / 16000 hz / 16 bit / .wav /

"""

def CheckFoldExist(foldpath):
    if os.path.exists(foldpath):
        return True
    else:
        return False
def GenFolder(foldpath):
    if(not CheckFoldExist(foldpath)):
        os.makedirs(foldpath)

def make_audio_file(source_path, destination_path):
    try:
        audio = GetAudio(source_path)
        audio = remove_Silence(audio)
        audio.export(f"{destination_path}.wav")
    except Exception as e:
        print("오류 발생:", e)

if __name__ == "__main__":
    base = "zeroth_korean"
    newbase = os.path.join(current_dir,"zeroth_korean_dataset")
    GenFolder(newbase)
    GenFolder(os.path.join(newbase,"train"))
    GenFolder(os.path.join(newbase,"test"))
    for usage in  [os.path.join('test_data_01',"003"),os.path.join('train_data_01',"003")]:
        path = os.path.join(current_dir,base,usage)
        newpath = 'train'
        if(usage == os.path.join("test_data_01","003")):
            newpath ='test'
        with open(os.path.join(newbase,newpath,newpath+'.txt'), "w",encoding="utf-8") as label:
            for folder in os.listdir(os.path.join(current_dir,base,usage)):
                for file in os.listdir(os.path.join(path,folder)):
                    filename, file_extension = os.path.splitext(file)
                    if(file_extension == '.txt'):
                        with open(os.path.join(path,folder,file), "r",encoding="utf-8") as existing_file:
                            label.write(existing_file.read())
                    else:
                        make_audio_file(os.path.join(path,folder,file),os.path.join(newbase,newpath,filename))