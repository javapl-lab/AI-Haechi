import WordRank

data_file_path = r'C:\Users\wlfkr\Desktop\seminar\datasetAst\block number dependency\0.txt'

solidity_file = open(data_file_path, 'r').read().split('  ')
index_file = bWordRank.word_to_index

for empty in solidity_file:
    if empty == '':
        solidity_file.remove(empty)

print('solidity_file:', solidity_file)

encoded_sentences = []
for word in solidity_file:
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
