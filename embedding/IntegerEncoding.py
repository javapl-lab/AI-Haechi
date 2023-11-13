import WordRank
import os

filename = '0'
abstract_result_path = os.path.abspath('../result/')

cfg_file = open(abstract_result_path + '/cfg/' + filename, 'r').read()
index_file = WordRank.zero_to_one
print(cfg_file)


# 특징부 추출
for str in cfg_file.split('\n'):
    # 전체 cfg에서 특징부만 걸러냄
    if (str.find("[label") == -1 and str.find("->") == -1 and
            str.find("->") == -1 and str.find("digraph G {") == -1 and
            str.find("node[shape=box, style=rounded") == -1) and str.find("}") == -1:
        # 불필요한 부분 제거
        str = str.replace('"];', '')
        str = str.replace('", shape = diamond];', '')
        print(str)

        # 치환 작업
        list = str.split(" ")
        feature_list = []

        for feature in list:
            number = WordRank.zero_to_one[feature]
            feature_list.append(number)

        print(feature_list)


#
# encoded_sentences = []
# for word in cfg_file:
#     encoded_sentence = []
#     try:
#         encoded_sentence.append(index_file[word])
#     except KeyError:
#         encoded_sentence.append(index_file['OOV'])
#     encoded_sentences.append(encoded_sentence)
#
#
# target_file_path = r'C:\Users\wlfkr\Desktop\encoded_solidity.result'
# result = open(target_file_path + '.result', 'w+')
# result.write(str(encoded_sentences))
# result.close()
# print('done')
