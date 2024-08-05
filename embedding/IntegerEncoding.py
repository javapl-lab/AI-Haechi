import WordRank

index_file = WordRank.zero_to_one

# 특징부 추출
for token in index_file.split('\n'):
    # 전체 cfg에서 특징부만 걸러냄
    if (token.find("[label") == -1 and token.find("->") == -1 and
            token.find("->") == -1 and token.find("digraph G {") == -1 and
            token.find("node[shape=box, style=rounded") == -1) and str.find("}") == -1:
        # 불필요한 부분 제거
        token = token.replace('"];', '')
        token = token.replace('", shape = diamond];', '')
        print(token)

        # 치환 작업
        token_list = token.split(" ")
        feature_list = []

        for feature in token_list:
            number = WordRank.zero_to_one[feature]
            feature_list.append(number)

        print(feature_list)
