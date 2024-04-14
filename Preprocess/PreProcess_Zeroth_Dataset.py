import os

"""
Zeroth Data set[https://www.openslr.org/40/] 폴더구조를 다음과 같의 재정의

```bash
├── train
│   ├── train.txt
│   ├── audiofiles
├── test
    ├── test.txt
    ├── audiofiles
``` 

"""



def CheckFoldExist(foldpath):
    if os.path.exists(foldpath):
        return True
    else:
        return False
    
def GenFolder(foldpath):
    if(not CheckFoldExist(foldpath)):
        os.makedirs(foldpath)

def move_audio_file(source_path, destination_path):
    try:
        os.replace(source_path, destination_path)
    except Exception as e:
        print("오류 발생:", e)

base = "zeroth_korean"
newbase = os.path.join(os.getcwd(),"zeroth_korean_dataset")
GenFolder(newbase)
GenFolder(os.path.join(newbase,"train"))
GenFolder(os.path.join(newbase,"test"))

for usage in  [os.path.join('test_data_01',"003"),os.path.join('train_data_01',"003")]:
    path = os.path.join(os.getcwd(),base,usage)
    newpath = 'train'
    if(usage == os.path.join("test_data_01","003")):
        newpath ='test'
    with open(os.path.join(newbase,newpath,newpath+'.txt'), "w") as label:
        for folder in os.listdir(os.path.join(os.getcwd(),base,usage)):
            for file in os.listdir(os.path.join(path,folder)):
                filename, file_extension = os.path.splitext(file)
                if(file_extension == '.txt'):
                    with open(os.path.join(path,folder,file), "r") as existing_file:
                        label.write(existing_file.read())
                else:
                    move_audio_file(os.path.join(path,folder,file),os.path.join(newbase,newpath,file))