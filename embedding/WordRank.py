import ast
import os

filename = 'WordFrequency.txt'
abstract_result_path = os.path.abspath('../result/embedding')

integer_encoding = open(abstract_result_path + '/' + filename, 'r').read()
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

integer_index_encoding = open(abstract_result_path + '/' + 'WordRank.txt', 'w+')
integer_index_encoding.write(str(word_to_index))
integer_index_encoding.close()

#==================================================
length = len(word_to_index)
zero_to_one = {}
for word in word_to_index:
    zero_to_one[word] = (word_to_index[word] - 1)/ (length - 1)

print(zero_to_one)
x = open(abstract_result_path + '/' + 'test.txt', 'w+')
x.write(str(zero_to_one))
x.close()
