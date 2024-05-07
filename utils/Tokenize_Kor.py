import numpy as np

def isKoUni(char):
    return ord('가')<=ord(char)<=ord('힣')

def isVowel(char):
    if(char == ''):
        return False
    return ord('ㅏ')<=ord(char)<=ord('ㅣ')

def isConstant(char):
    if(char == ''):
        return False
    return ord('ㄱ')<=ord(char)<=ord('ㅎ')

def Decompose_initialConstant(char):
    initial_list = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    initial_index = (ord(char) - ord('가')) // 588 
    if(initial_index >=0):
        return initial_list[initial_index]
    return ''

def Decompose_vowel(char):
    if(char == ' '):
        return ' '
    vowel_list = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
    vowel_index = ((ord(char) - ord('가')) % 588) // 28 
    if(vowel_index>=0):
        return vowel_list[vowel_index]
    return ''

def Decompose_finalConstant(char):
    if(char == ' '):
        return ' '
    final_list = ['ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    final_index = ((ord(char) - ord('가')) % 28) - 1
    if final_index >= 0:
        return final_list[final_index]
    return ''


def 구개음화(char1,char2,char3):
    vowel_list = [ 'ㅑ', 'ㅒ', 'ㅕ', 'ㅖ','ㅛ', 'ㅠ', 'ㅣ']
    if(isConstant(char1) and char2 == 'ㅇ' and (char3 in vowel_list)):
        if(char1 =='ㄷ'):
            char1 = ''
            char2 = 'ㅈ'
        elif(char1 =='ㅌ'):
            char1 = ''
            char2 = 'ㅊ'
        elif(char1 =='ㄾ'):
            char1 = 'ㄹ'
            char2 = 'ㅊ'
    return [char1,char2,char3]

def 연음화(char1,char2):
    if(isConstant(char1) and char2 == 'ㅇ'):
        if(char1 =='ㄳ'):
            char1 = 'ㄱ'
            char2 = 'ㅅ'
        elif(char1 =='ㄵ'):
            char1 = 'ㄴ'
            char2 = 'ㅈ'
        elif(char1 =='ㄶ'):
            char1 = ''
            char2 = 'ㄴ'
        elif(char1 =='ㄻ'):
            char1 = 'ㄹ'
            char2 = 'ㅁ'
        elif(char1 =='ㄺ'):
            char1 = 'ㄹ'
            char2 = 'ㄱ'
        elif(char1 =='ㄼ'):
            char1 = 'ㄹ'
            char2 = 'ㅂ'
        elif(char1 =='ㄽ'):
            char1 = 'ㄹ'
            char2 = 'ㅅ'
        elif(char1 =='ㄾ'):
            char1 = 'ㄹ'
            char2 = 'ㅌ'
        elif(char1 =='ㄿ'):
            char1 = 'ㄹ'
            char2 = 'ㅍ'
        elif(char1 =='ㅀ'):
            char1 = ''
            char2 = 'ㄹ'
        elif(char1 =='ㅄ'):
            char1 = 'ㅂ'
            char2 = 'ㅅ'
        elif(char1 =='ㅎ'):
            char1 = ''  
        elif(char1 != 'ㅇ'):
            char2 = char1
            char1 = ''
    return [char1,char2]

def 된소리되기(char1,char2):
    if(isConstant(char1) and isConstant(char2)):
        if(char1 =='ㄱ' or char1 =='ㄷ' or char1 =='ㅂ'):
            if(char2 =='ㄱ'):
                char2 = 'ㄲ'
            if(char2 =='ㄷ'):
                char2 = 'ㄸ'
            if(char2 =='ㅂ'):
                char2 = 'ㅃ'             
            if(char2 =='ㅅ'):
                char2 = 'ㅆ'     
            if(char2 =='ㅈ'):
                char2 = 'ㅉ'     
    return [char1,char2]

def 거센소리되기(char1,char2):
    if(isConstant(char1)and isConstant(char2)):
        if(char2 =='ㅎ'):
            if(char1 =='ㄱ'):
                char1 = ''
                char2 = 'ㅋ'
            elif(char1 =='ㄷ'):
                char1 = ''
                char2 = 'ㅌ'
            elif(char1 =='ㅂ'):
                char1 = ''
                char2 = 'ㅍ'
            elif(char1 =='ㅈ'):
                char1 = ''
                char2 = 'ㅊ'
            elif(char1 =='ㄵ'):
                char1 = 'ㄴ'
                char2 = 'ㅊ'
            elif(char1 =='ㄺ'):
                char1 = 'ㄹ'
                char2 = 'ㅋ'
            elif(char1 =='ㄼ'):
                char1 = 'ㄹ'
                char2 = 'ㅍ'
        if(char1 =='ㅎ' or char1 =='ㅀ' or char1 =='ㄶ'):
            flag = 0
            if(char2 =='ㄱ'):
                char2 = 'ㅋ'
                flag = 1
            elif(char2 =='ㄷ'):
                char2 = 'ㅌ'
                flag = 1
            elif(char2 =='ㅂ'):
                char2 = 'ㅍ'
                flag = 1
            elif(char2 =='ㅈ'):
                char2 = 'ㅊ'
                flag = 1
            if(flag == 1):
                if(char1 =='ㅀ'):
                    char1 = 'ㄹ'
                elif(char2 =='ㄶ'):
                    char1 = 'ㄴ'
                else:
                    char1 =''
    return [char1,char2]


def 자음단순화(char1,char2):
    if(isConstant(char1) and isConstant(char2)):
        if(char1 =='ㄳ'):
            char1 = 'ㄱ'
        elif(char1 =='ㄵ'):
            char1 = 'ㄴ'
        elif(char1 =='ㄶ'):
            char1 = 'ㄴ'
        elif(char1 =='ㄺ'):
            char1 = 'ㄹ'
        elif(char1 =='ㄻ'):
            char1 = 'ㄹ'
        elif(char1 =='ㄼ'):
            char1 = 'ㄹ'
        elif(char1 =='ㄽ'):
            char1 = 'ㄹ'
        elif(char1 =='ㄾ'):
            char1 = 'ㄹ'
        elif(char1 =='ㄿ'):
            char1 = 'ㄹ'
        elif(char1 =='ㅀ'):
            char1 = 'ㄹ'
        elif(char1 =='ㅄ'):
            char1 = 'ㅂ'
    return [char1,char2]


def 음절의끝소리규칙(char1,char2):
    if(isConstant(char1) and isConstant(char2)):
        if(char2 != 'ㅇ'):
            if(char1=='ㄲ'):
                char1 = 'ㄱ'
            elif(char1=='ㅋ'):
                char1 = 'ㄱ'
            elif(char1=='ㅌ'):
                char1='ㄷ'
            elif(char1 == 'ㅅ'):
                char1 = 'ㄷ'
            elif(char1 == 'ㅆ'):
                char1 = 'ㄷ'
            elif(char1 == 'ㅈ'):
                char1 ='ㄷ'
            elif(char1 =='ㅊ'):
                char1= 'ㄷ'
            elif(char1 =='ㅎ'):
                char1= 'ㄷ'
            elif(char1=='ㅍ'):
                char1 = 'ㅂ'  
    return [char1,char2]


def 비음화(char1,char2):
    if(isConstant(char1) and isConstant(char2)):
        if(char2 == 'ㅁ' or char2 =='ㄴ' or char2 =='ㄹ'):
            if(char1 =='ㅂ'):
                char1 = 'ㅁ'
            elif(char1=='ㄷ'):
                char1 = 'ㄴ'
            elif(char1 =='ㄱ'):
                char1 = 'ㅇ'
        if(char1 == 'ㅁ' or char1 =='ㅇ'):
            if(char2=='ㄹ'):
                char2 = 'ㄴ' 
    return [char1,char2]

def 유음화(char1,char2):
    if(isConstant(char1) and isConstant(char2)):
        if(char1=='ㄹ' and char2=='ㄴ'):
            char2 = 'ㄹ'
        elif(char1=='ㄴ' and char2 =='ㄹ'):
            char1 ='ㄹ'
    return [char1,char2]


def decompose_tokens(text):
    result = []
    phoneme_index = []
    for i, c in enumerate(text):
        if(isKoUni(c)):
            initial = Decompose_initialConstant(c)
            vowel = Decompose_vowel(c)
            final = Decompose_finalConstant(c)
            if(initial != ""):
                phoneme_index.append(i)
                result.extend(initial)
            if(vowel != ""):
                phoneme_index.append(i)
                result.extend(vowel)
            if(final != ""):
                phoneme_index.append(i)
                result.extend(final)
        elif(c == ' '):
            phoneme_index.append(i)
            result.extend(c)

    length = len(result)
    for i in range(length):
        if(result[i] == ' '):
            continue
        if(i+1<length):
            result[i], result[i+1]= 거센소리되기(result[i],result[i+1])
            result[i], result[i+1]= 음절의끝소리규칙(result[i],result[i+1])
            result[i], result[i+1]= 비음화(result[i],result[i+1])
            result[i], result[i+1]= 유음화(result[i],result[i+1])
            result[i], result[i+1]= 연음화(result[i],result[i+1])
            result[i], result[i+1]= 자음단순화(result[i],result[i+1])
        if(i+2 <length):
            result[i], result[i+1], result[i+2] = 구개음화(result[i],result[i+1],result[i+2])
        if(i+1<length):
            result[i], result[i+1]= 된소리되기(result[i],result[i+1])

    while '' in result:
        index = result.index('')
        del result[index]
        del phoneme_index[index]
    return [result , phoneme_index]


def GetUniChar(init,vowel,final = None):
    initial_list = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    vowel_list = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
    final_list = ['ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

    initindex = initial_list.index(init)
    midindex = vowel_list.index(vowel) 
    endindex = -1
    if(final is not None):
        endindex = final_list.index(final) 
    initcount = ord('가') + initindex*len(vowel_list)*(len(final_list)+1)
    midcount = (len(final_list)+1)*midindex
    endcount = endindex
    return(chr(initcount+midcount+endcount+1))

def compoes_tokens(decomposed):
    result = []
    decomposed_str = "".join(decomposed)
    decomposed_str_list = decomposed_str.split(' ')
    for tokens in decomposed_str_list:
        start = 0
        length = len(tokens)
        for i, v in enumerate(tokens):
            if (i == length-1 or i-start == 3):
                if(i-start >= 2 and isConstant(tokens[i])):
                    result.extend(GetUniChar(tokens[start],tokens[start+1],tokens[start+2]))
                    start = start+3
                else:
                    result.extend(GetUniChar(tokens[start],tokens[start+1]))
                    start = start+2
                    if(i == length-1 and start != length):
                        result.extend(GetUniChar(tokens[start],tokens[start+1]))
        if(tokens != decomposed_str_list[-1]):
            result.extend(' ')
    return result

