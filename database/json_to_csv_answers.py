import pandas as pd
import json
import os

# JSON 파일 경로 설정
json_dir = 'C:/Users/82109/Downloads/111.수학 과목 문제생성 데이터/3.개방데이터/1.데이터/Validation/02.라벨링데이터/VL_2.모범답안_중학교_3학년'
output_csv = 'output_answers3_val.csv'  # 생성할 CSV 파일 이름

# 모든 JSON 파일을 읽어 원하는 데이터 추출
extracted_data = []

# 모든 JSON 파일을 탐색
json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
for json_file in json_files:
    file_path = os.path.join(json_dir, json_file)
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

        # 문제 ID와 답안 파일명 추출
        question_id = data['id']
        
        # answer_info 배열에서 첫 번째 요소를 가져옴
        if data['answer_info']:
            answer_info = data['answer_info'][0]  # 첫 번째 요소
            answer_filename = answer_info['answer_filename']
            answer_text = answer_info['answer_text']  # answer_text는 그대로 사용
            
            # answer_bbox에서 type이 'answer'인 경우의 text 추출
            answer_correct = None  # 기본값은 None
            for bbox in answer_info['answer_bbox']:
                if bbox['type'] == 'answer':
                    answer_correct = bbox['text']  # 'answer' 타입의 text

            # 추출된 데이터를 리스트에 추가
            extracted_data.append({
                'question_id': question_id,
                'answer_filename': answer_filename,
                'answer_text': answer_text,
                'answer_correct': answer_correct,  # 'answer' 타입의 text
                'source': '111.수학 과목 문제생성 데이터',  # 새로운 source 열 추가
                'label': 'validation'                     # 새로운 label 열 추가
            })

# DataFrame으로 변환
df = pd.DataFrame(extracted_data)

# CSV 파일로 저장
df.to_csv(output_csv, index=False, encoding='utf-8')
