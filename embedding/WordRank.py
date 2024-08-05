import ast

def word_rank(file_path, result_path):
    WordFrequncy = open(file_path + '/WordFrequency.txt', 'r').read()
    WordFrequncy = ast.literal_eval(WordFrequncy)
    
    max_token_rank = 1000
    # 대체할 단어의 빈도수를 임의로 설정
    oov_frequncy = 5
    
    word_rank_dict = {}
    rank = 1
    for word, frequncy in WordFrequncy:
        word_rank_dict[word] = [rank, frequncy]
        rank += 1
        
        if rank == max_token_rank:
            break
            

    word_rank_dict['OOV'] = [max_token_rank, oov_frequncy]

    WordRank = open(result_path + '/WordRank.txt', 'w+')
    WordRank.write(str(word_rank_dict))
    WordRank.close()
    
    return word_rank_dict