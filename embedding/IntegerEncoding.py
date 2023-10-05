import WordRank
import os

filename = 'for_code'
abstract_result_path = os.path.abspath('../Graph_generator_for_GNN/result/')

cfg_file = open(abstract_result_path + 'cfg_img/' + filename, 'r').read().split('  ')
index_file = WordRank.word_to_index

for empty in cfg_file:
    if empty == '':
        cfg_file.remove(empty)

print('cfg_file:', cfg_file)

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
