# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ 특징 생성 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
def create_feature(node):
    feature = ""

    for key, value in node.items():
        if isinstance(value, dict):
            feature += create_feature(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    feature += create_feature(item)

        elif isinstance(value, str):
            if key == 'name':
                feature += value + ' '
            if key == 'operator':
                feature += value + ' '
            if key == 'number':
                feature += value + ' '
            if key == 'visibility':
                feature += value + ' '
        elif isinstance(value, bool):
            if key == 'isPrefix':
                if value:
                    feature += "Prefix Operator"
                else:
                    feature += "Postfix Operator"
            '''다른 추가적인 정보 담아야함'''

    return feature
