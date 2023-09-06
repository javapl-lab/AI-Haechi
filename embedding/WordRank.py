import ast

file_path = r'C:\Users\wlfkr\Desktop' + '\\' + 'IntegerEncoding.txt'
integer_encoding = open(file_path, 'r').read()
integer_encoding = ast.literal_eval(integer_encoding)


word_to_index = {}
i = 1
for word, frequency in integer_encoding:
    if frequency > 20:
        word_to_index[word] = i
        i += 1

word_to_index['OOV'] = len(word_to_index) + 1
print(word_to_index)

target_file_path = r'C:\Users\wlfkr\Desktop' + '\\' + 'integer_index_encoding'
integer_index_encoding = open(target_file_path + '.txt', 'w+')
integer_index_encoding.write(str(word_to_index))
integer_index_encoding.close()

