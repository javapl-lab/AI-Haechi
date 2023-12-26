import pandas as pd

# CSV 파일 경로 설정
csv_file_path = './learning/ground truth label.csv'  # 또는 'csv' 파일 확장자일 수도 있습니다.

# 모든 시트를 읽기
excel_data = pd.read_excel(csv_file_path, sheet_name=None)
new_data = pd.DataFrame(columns=['folder' ,'file', 'ground truth'])

number = 1
index = 0

weakness_name = ['block number dependency', 'dangerous delegatecall', 'ether frozen', 'ether strict equality',
                 'integer overflow', 'reentrancy', 'timestamp dependency', 'unchecked external call']
tmp = ['unchecked external call']

# 각 시트의 데이터 출력
for weakness in tmp:
    for sheet_name, sheet_data in excel_data.items():
        if sheet_name == weakness:
            print(f"Sheet: {sheet_name} : {number}")



            for file_value, group in sheet_data.groupby('file'):
                if any(group['ground truth'] == 1):
                    new_data.loc[index] = [sheet_name, file_value, 1]
                else:
                    new_data.loc[index] = [sheet_name, file_value, 0]

                index += 1
            new_data.to_csv(f'./learning/output_{weakness}.csv', index=False)
            number += 1




