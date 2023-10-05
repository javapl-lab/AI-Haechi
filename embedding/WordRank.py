import ast
import os

filename = 'IntegerEncoding.txt'
abstract_result_path = os.path.abspath('../result/')

integer_encoding = open(abstract_result_path + 'embedding/' + filename, 'r').read()
integer_encoding = ast.literal_eval(integer_encoding)
print(integer_encoding)


word_to_index = {}
i = 1
for word, frequency in integer_encoding:
    if frequency > 20:
        word_to_index[word] = i
        i += 1

word_to_index['OOV'] = len(word_to_index) + 1
print(word_to_index)

integer_index_encoding = open(abstract_result_path + 'embedding/' + 'integer_index_encoding_result', 'w+')
integer_index_encoding.write(str(word_to_index))
integer_index_encoding.close()

