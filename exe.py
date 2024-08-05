import os
os.environ["DGLBACKEND"] = "pytorch"

import sys
sys.path.insert(0, '/workspace/sku3343/heesung')

import torch
from parsing.Generator import generate

file_path = os.path.abspath('../sku3343/dataset/solidity/block number dependency')
result_path = os.path.abspath('../sku3343/dataset/')

solidity_code_path = os.path.abspath('../sku3343/dataset/solidity/block number dependency/')
g = generate(file_path, '127.sol', result_path)
model = torch.load(os.path.abspath('../sku3343/heesung/model'), map_location=torch.device('cpu'))
pred = model(g)

print(pred)
