from Tokenize_Kor import isVowel
def CalPenality(s1,s2):
    penalty = 1
    s1_vowel = isVowel(s1)
    s2_vowel = isVowel(s2)
    if(s1_vowel == s2_vowel):
        penalty = 0.5
    else:
        if(s1 == 'ㅇ' or s2=='ㅇ'):
            penalty = 0.5
    return penalty

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
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + CalPenality(s1[i-1],s2[j-1])
    return dp

def Expand_Dist_Matrix(mat , s1, s2):
    m , n  = len(mat), len(mat[0])
    dp = np.pad(mat, ((0, 1), (0, 1)), mode='constant', constant_values=0)
    dp[m][0] = m
    dp[0][n] = n
    for i in range(1, m):
        if s1[i-1] == s2[n-1]:
            dp[i][n] = dp[i-1][n-1]
        else:
            dp[i][n] = min(dp[i-1][n], dp[i][n-1], dp[i-1][n-1]) + CalPenality(s1[i-1],s2[n-1])
    for j in range(1, n):
        if s1[m-1] == s2[j-1]:
            dp[m][j] = dp[m-1][j-1]
        else:
            dp[m][j] = min(dp[m][j-1], dp[m-1][j], dp[m-1][j-1])+ CalPenality(s1[m-1],s2[j-1])
    if s1[m-1] == s2[n-1]:
        dp[m][n] = dp[m-1][n-1]
    else:
        dp[m][n] = min(dp[m-1][n-1], dp[m][n-1], dp[m-1][n]) + CalPenality(s1[m-1],s2[n-1])
    return dp

import numpy as np
def PhonemeMatching(origintext,predtext):
    matching = [] 
    s1_len = len(origintext)
    s2_len = len(predtext)
    s1_index = 0
    s2_index = 0
    isMinIndice = False
    exec = True
    while(exec):
        size = 2
        dist_mat = levenshtein_distance_Marix(origintext[s1_index:s1_index+size], predtext[s2_index:s2_index+size])
        min_indices = np.empty(0)
        if( s1_index + size >= s1_len or s2_index + size >= s2_len):
            matching.append([s1_index,s2_index,s1_len,s2_len])
            exec = False
            break
        candi = np.concatenate([dist_mat[size,:size+1],dist_mat[:size,size]])
        min_indices = np.where(candi == np.min(candi))[0]
        isMinIndice = (min_indices.size == 1)
        while (not isMinIndice):
            if( s1_index + size >= s1_len or s2_index + size >= s2_len):
                matching.append([s1_index,s2_index,s1_len,s2_len])
                exec = False
                break
            dist_mat = Expand_Dist_Matrix(dist_mat,origintext[s1_index:s1_index+size+1], predtext[s2_index:s2_index+size+1])
            candi = np.concatenate([dist_mat[size,:size+1],dist_mat[:size,size]])
            min_indices = np.where(candi == np.min(candi))[0]
            isMinIndice = (min_indices.size == 1)
            if(not isMinIndice):
                size +=1
        if(exec):
            min_indices = min_indices[0]
            if(min_indices <= size):
                matching.append([s1_index,s2_index,s1_index+size,s2_index+min_indices])  
                s1_index = s1_index+size
                s2_index = s2_index+min_indices
            else:
                matching.append([s1_index,s2_index,s1_index+min_indices,s2_index+size])  
                s1_index = s1_index+min_indices
                s2_index = s2_index+size
    for i, v in enumerate(matching):
        print("origin:" ,origintext[v[0]:v[2]],"pred:", predtext[v[1]:v[3]])

from Tokenize_Kor import decompose_tokens
origin = "안녕하세요"
pred = "아안녀엉하세에요오"
PhonemeMatching(decompose_tokens(origin),decompose_tokens(pred))