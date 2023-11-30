import pandas as pd

# CSV 파일 경로 설정
csv_file_path = './learning/ground truth label.csv'  # 또는 'csv' 파일 확장자일 수도 있습니다.

# 모든 시트를 읽기
excel_data = pd.read_excel(csv_file_path, sheet_name=None)
new_data = pd.DataFrame(columns=['folder' ,'file', 'ground truth'])

number = 1
index = 0

# 각 시트의 데이터 출력
for sheet_name, sheet_data in excel_data.items():
    print(f"Sheet: {sheet_name} : {number}")



    for file_value, group in sheet_data.groupby('file'):
        if any(group['ground truth'] == 1):
            new_data.loc[index] = [sheet_name, file_value, number]
        else:
            new_data.loc[index] = [sheet_name, file_value, 0]

        index += 1

    number += 1

# 결과 출력
print(new_data)
new_data.to_csv('./learning/output.csv', index=False)

