import os
from WordFrequency import word_frequency
from WordRank import word_rank
from Normalization import normalization

file_path = os.path.abspath('../sku3343/dataset/')
result_path = os.path.abspath('../sku3343/dataset/')

# word_frequency(file_path, result_path)
word_rank_dict = word_rank(file_path, result_path)
normalization(word_rank_dict, result_path)