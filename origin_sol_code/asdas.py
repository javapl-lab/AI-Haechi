import pandas as pd

# CSV 파일 경로 설정
csv_file_path = 'ground truth label.csv'  # 또는 'csv' 파일 확장자일 수도 있습니다.

# 모든 시트를 읽기
excel_data = pd.read_excel(csv_file_path, sheet_name=None)

# 각 시트의 데이터 출력
for sheet_name, sheet_data in excel_data.items():
    print(f"Sheet: {sheet_name}")
    print(sheet_data)
