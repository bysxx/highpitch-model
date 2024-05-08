import sys,os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
current_dir = os.path.dirname(os.path.abspath(__file__))
from utils.Audio import PrintAudioInfo, GetAudio, remove_Silence

from utils.Tokenize_Kor import isVowel
import numpy as np


def CalPenality(s1,s2 , i , j):
    c1 = s1[i]
    c2 = s2[j]
    s2_len = len(s2)
    penalty = 1
    c1_vowel = isVowel(c1)
    c2_vowel = isVowel(c2)
    if(c1_vowel == c2_vowel):
        penalty = 0.5
        # 조음 위치가 비슷한 음소는 패널티를 적게 부여하자..
        # if((c1 =='ㅈ') and (c2 == 'ㅉ')):
        #     penalty = 0.3
    else:
        if(c1_vowel and (c2=='ㅇ')):
            penalty = 0.2
    return penalty

def findpath(mat,i,j ,dp):
    left = i>1
    up = j >1
    diag = left and up
    if not (left or up):
        return [[[i,j]] , mat[i][j]]
    else:
        candi = []
        if(left):
            candi.append(mat[i-1][j])
        else:
            candi.append(np.inf)
        if(diag):
            candi.append(mat[i-1][j-1])
        else:
            candi.append(np.inf)
        if(up):
            candi.append(mat[i][j-1])
        else:
            candi.append(np.inf)
        min_indices = np.where(candi == np.min(candi))[0]

        candipath = []
        candi_pred = []
        for index in min_indices:
            candi_row  = i 
            candi_col = j
            if(index==0):
                candi_row = i-1
            if(index==1):
                candi_row = i-1
                candi_col = j-1
            if(index==2):
                candi_col = j-1
            if(dp[candi_row][candi_col] == None):
                dp[candi_row][candi_col] = findpath(mat,candi_row,candi_col,dp)
            candipath.append(dp[candi_row][candi_col][0])
            candi_pred.append(dp[candi_row][candi_col][1])
        min_indices = np.where(candi_pred == np.min(candi_pred))[0]
        path = [[i,j]]
        path.extend(candipath[min_indices[0]])
        return [path , mat[i][j]+candi_pred[min_indices[0]]]

def levenshtein_distance_Marix(s1, s2):
    m, n = len(s1), len(s2)
    # DP 테이블 초기화
    dp = np.zeros((m+1, n+1))
    # DP 테이블 첫 번째 행과 열 초기화
    for i in range(1, m+1):
        dp[i][0] = i
    for j in range(1, n+1):
        dp[0][j] = j
    # DP 테이블 채우기
    for i in range(1, m+1):
        for j in range(1, n+1):
            dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
            if s1[i-1] != s2[j-1]:
                dp[i][j]  += CalPenality(s1,s2,i-1,j-1)
    return dp

def infer(s1, s2):
    mat = levenshtein_distance_Marix(s1,s2)
    dp =  np.full(mat.shape, None)
    i,j = len(s1), len(s2) 
    path , cost =  findpath(mat,i,j,dp)
    result = path[::-1]
    inferedresult = [[result[0][0],[result[0][1]]]]
    for i in range(1,len(result)):
        prev_index = result[i-1][0]-1
        index = result[i][0]-1
        if(prev_index == index):
            inferedresult[prev_index][1].append(result[i][1])
        else:
            inferedresult.append([result[i][0],[result[i][1]]])
    return inferedresult







