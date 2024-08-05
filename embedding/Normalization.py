import numpy as np

def normalization(word_rank_dict, result_path):
    freqs = np.array([freq for idx, freq in word_rank_dict.values()])

    # # 중앙값과 IQR 계산
    median = np.median(freqs)
    q1 = np.percentile(freqs, 25)
    q3 = np.percentile(freqs, 75)
    iqr = q3 - q1

    robust_dict = {word: (freq - median) / iqr for word, [idx, freq] in word_rank_dict.items()}

    # 값만 추출
    values = list(robust_dict.values())

    # 최소값과 최대값 계산
    min_val = min(values)
    max_val = max(values)

    # 최소-최대 정규화 수행
    min_max_dict = {word: (value - min_val) / (max_val - min_val) for word, value in robust_dict.items()}
        
    Normalization = open(result_path + '/Normalization.txt', 'w+')
    Normalization.write(str(min_max_dict))
    Normalization.close()