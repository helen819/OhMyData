import pandas as pd
import json
import os

# JSON 파일 경로 설정
json_dir = 'C:/Users/82109/Downloads/111.수학 과목 문제생성 데이터/3.개방데이터/1.데이터/Validation/02.라벨링데이터/VL_1.문제_중학교_3학년'
output_csv = 'output_questions3_val.csv'  # 생성할 CSV 파일 이름

# 모든 JSON 파일을 읽어 원하는 데이터 추출
extracted_data = []

# 모든 JSON 파일을 탐색
json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
for json_file in json_files:
    file_path = os.path.join(json_dir, json_file)
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

        # 문제 ID와 파일명 추출
        question_filename = data['question_filename']
        question_id = data['id']

        # question_info 배열에서 첫 번째 요소를 가져옴
        if data['question_info']:
            question_info = data['question_info'][0]  # 첫 번째 요소
            question_grade = question_info['question_grade']
            question_term = question_info['question_term']
            question_unit = question_info['question_unit']
            question_topic = question_info['question_topic']
            question_topic_name = question_info['question_topic_name']
            question_type1 = question_info['question_type1']
            question_type2 = question_info['question_type2']
            question_condition = question_info['question_condition']
            question_step = question_info['question_step']
            question_sector1 = question_info['question_sector1']
            question_sector2 = question_info['question_sector2']
            question_difficulty = question_info['question_difficulty']
            question_contents = question_info.get('question_contents', 0)  # 기본값 0
        else:
            question_grade = question_term = question_unit = question_topic = None
            question_topic_name = question_type1 = question_type2 = None
            question_condition = question_step = question_sector1 = question_sector2 = None
            question_difficulty = None
            question_contents = 0

        # OCR_info 배열에서 첫 번째 요소를 가져옴
        if data['OCR_info']:
            ocr_info = data['OCR_info'][0]  # 첫 번째 요소
            figure_text = ocr_info.get('figure_text', None)  # Optional
            question_text = ocr_info['question_text']
        else:
            figure_text = None
            question_text = None

        # 추출된 데이터를 리스트에 추가
        extracted_data.append({
            'question_id': question_id,
            'question_filename': question_filename,
            'question_grade': question_grade,
            'question_term': question_term,
            'question_unit': question_unit,
            'question_topic': question_topic,
            'question_topic_name': question_topic_name,
            'question_type1': question_type1,
            'question_type2': question_type2,
            'question_condition': question_condition,
            'question_step': question_step,
            'question_sector1': question_sector1,
            'question_sector2': question_sector2,
            'question_difficulty': question_difficulty,
            'question_contents': question_contents,
            'figure_text': figure_text,
            'question_text': question_text,
            'source': '111.수학 과목 문제생성 데이터',  # 새로운 source 열 추가
            'label': 'validation'                     # 새로운 label 열 추가
        })

# DataFrame으로 변환
df = pd.DataFrame(extracted_data)

# CSV 파일로 저장
df.to_csv(output_csv, index=False, encoding='utf-8')
