import sys,os
current_dir = os.getcwd()
sys.path.append(os.path.dirname(os.path.abspath(current_dir)))

def MakeLyricInfo(name,label):
    audio_path = os.path.join(current_dir,f'{name}.wav')
    result = model(audio_path, label)
    audio = GetAudio(audio_path)
    length = len(result)
    for i , w in enumerate(result):
        silentlist = []
        if(i<length-1):
            if(w['end'] != result[i+1]['start']):
                silentlist = detect_silence(audio[w['end']*1000:result[i+1]['start']*1000],min_silence_len=100,silence_thresh=-30)
                if(silentlist):
                    w['end'] = w['end']+  silentlist[0][0]/1000
                else:
                    w['end'] = result[i+1]['start']

        else:
            silentlist = detect_silence(audio[w['end']*1000:],min_silence_len=100,silence_thresh=-30)
            if(silentlist):
                w['end'] = w['end']+  silentlist[0][0]/1000
            else:
                w['end'] = audio.duration_seconds
    with open(f"{name}.json", 'w', encoding='utf-8') as LyricInfoFile:
        json.dump(result, LyricInfoFile)
    return result

if __name__ == '__main__':
    from Model_Vocals import Model_Vocals
    import json
    from pydub.silence import detect_silence
    from pydub import AudioSegment
    from utils.Audio import GetAudio

    model = Model_Vocals()
    model.initialize(4)


    name = 'Wav/아기상어_윤종신_V'
    label = """
    아기상어
    뚜루루뚜루 
    귀여운 
    뚜루루뚜루 
    바닷속 
    뚜루루뚜루 
    아기상어! 
    엄마상어 
    뚜루루뚜루 
    어여쁜 
    뚜루루뚜루 
    바닷속 
    뚜루루뚜루 
    엄마상어! 
    아빠상어 
    뚜루루뚜루 
    힘이 센 
    뚜루루뚜루 
    바닷속
    뚜루루뚜루
    아빠상어!
    할머니상어
    뚜루루뚜루
    자상한
    뚜루루뚜루
    바닷속
    뚜루루뚜루
    할머니상어!
    할아
    할아버지 상어 뭐죠?
    할아버지상어
    뚜루루뚜루
    멋있는
    뚜루루뚜루
    바닷속
    뚜루루뚜루
    할아버지상어!
    우리는
    뚜루루뚜루
    바다의
    뚜루루뚜루
    사냥꾼
    뚜루루뚜루
    상어가족!
    상어다
    뚜루루뚜루
    도망쳐
    뚜루루뚜루
    도망쳐
    뚜루루뚜루
    숨자! 으악!
    살았다
    뚜루루뚜루
    살았다
    뚜루루뚜루
    오늘도
    뚜루루뚜루
    살았다! 
    신난다
    뚜루루뚜루
    신난다
    뚜루루뚜루
    춤을 춰
    뚜루루뚜루
    노래 끝! 오예!
    어 근데 약간 중독성 있는데 이노래?"""

    label = label.replace('\n',' ')
    result = MakeLyricInfo(name,label)


    name =os.path.join(current_dir,  'Wav','산중호걸_V')
    label = """

    산중호걸이라 하는
    호랑님의 생일날이 되어
    각색 짐승 공원에 모여
    무도회가 열렸네

    토끼는 춤추고
    여우는 바이올린
    찐짠 
    찌가찌가 찐짠
    찐짠찐짠하더라

    그 중에 한 놈이
    잘난 체하면서
    까불 
    까불까불 까불
    까불까불하더라

    """
    label = label.replace('\n',' ')
    result = MakeLyricInfo(name,label)


    name = os.path.join(current_dir, 'Wav','아기상어_V')
    label = """아기상어
    뚜루루뚜루 
    귀여운 
    뚜루루뚜루 
    바닷속 
    뚜루루뚜루 
    아기상어! 
    엄마상어 
    뚜루루뚜루 
    어여쁜 
    뚜루루뚜루 
    바닷속 
    뚜루루뚜루 
    엄마상어! 
    아빠상어 
    뚜루루뚜루 
    힘이 센 
    뚜루루뚜루 
    바닷속
    뚜루루뚜루
    아빠상어!
    할머니상어
    뚜루루뚜루
    자상한
    뚜루루뚜루
    바닷속
    뚜루루뚜루
    할머니상어!
    할아버지상어
    뚜루루뚜루
    멋있는
    뚜루루뚜루
    바닷속
    뚜루루뚜루
    할아버지상어!
    우리는
    뚜루루뚜루
    바다의
    뚜루루뚜루
    사냥꾼
    뚜루루뚜루
    상어가족!
    상어다
    뚜루루뚜루
    도망쳐
    뚜루루뚜루
    도망쳐
    뚜루루뚜루
    숨자! 으악!
    살았다
    뚜루루뚜루
    살았다
    뚜루루뚜루
    오늘도
    뚜루루뚜루
    살았다! 휴우~
    신난다
    뚜루루뚜루
    신난다
    뚜루루뚜루
    춤을 춰
    뚜루루뚜루
    노래 끝! 오예!"""

    label = label.replace('\n',' ')
    result = MakeLyricInfo(name,label)

    name =os.path.join(current_dir,  'Wav','멋쟁이토마토_V')
    label = """

    울퉁불퉁 멋진 몸매에
    빠알간 옷을 입고
    새콤달콤 향기 풍기는
    멋쟁이 토마토 (토마토)
    나는야 주스될거야 (꿀꺽)
    나는야 케찹될거야 (찍)
    나는야 춤을 출거야 (헤이)
    뽐내는 토마토 (토마토)

    울퉁불퉁 멋진 몸매에
    빠알간 옷을 입고
    새콤달콤 향기 풍기는
    멋쟁이 토마토 (토마토)
    나는야 주스될거야 (꿀꺽)
    나는야 케찹될거야 (찍)
    나는야 춤을 출거야 (헤이)
    뽐내는 토마토 (토마토)

    """
    label = label.replace('\n',' ')
    result = MakeLyricInfo(name,label)

    model.close_pool()