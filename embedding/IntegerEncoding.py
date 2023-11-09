import WordRank
import os

filename = 'for_code'
abstract_result_path = os.path.abspath('../result/')

cfg_file = open(abstract_result_path + '/cfg/' + filename, 'r').read().split('  ')
index_file = WordRank.word_to_index
print(index_file)
cfg_file = cfg_file[0]
print(cfg_file)

for empty in cfg_file:
    if empty == '':
        cfg_file.remove(empty)


encoded_sentences = []
for word in cfg_file:
    encoded_sentence = []
    try:
        encoded_sentence.append(index_file[word])
    except KeyError:
        encoded_sentence.append(index_file['OOV'])
    encoded_sentences.append(encoded_sentence)


target_file_path = r'C:\Users\wlfkr\Desktop\encoded_solidity.result'
result = open(target_file_path + '.result', 'w+')
result.write(str(encoded_sentences))
result.close()
print('done')
