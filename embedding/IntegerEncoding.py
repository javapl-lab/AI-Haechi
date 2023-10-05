import WordRank
import os

def integer_encoding(file_name):
    abstract_result_path = os.path.abspath('../Graph_generator_for_GNN/result/embedding/')

    solidity_file = open(abstract_result_path + file_name, 'r').read().split('  ')
    index_file = WordRank.word_to_index

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
