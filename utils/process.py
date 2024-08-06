import pandas as pd
import os, json, re

from openai import OpenAI
from utils import prompt

def json_to_dict():
    with open(f"diary/diary.json", 'r', encoding='utf-8') as file:
        return json.load(file)

def extract_closest_emotions(file_path: str, diary_score: float, num_emotions: int = 5) -> list:
    """
    주어진 파일 경로에서 CSV 파일을 로드하여 불쾌 수치가 가장 유사한 감정을 추출합니다.

    매개변수:
    file_path (str): CSV 파일의 경로.
    diary_score (float): 비교할 일기의 불쾌 수치.
    num_emotions (int, optional): 반환할 유사한 감정의 개수. 기본값은 5입니다.

    반환 값:
    list: 불쾌 수치가 가장 가까운 감정 단어 리스트.

    예외:
    TypeError: 데이터프레임을 로드하지 못한 경우 발생합니다.
    """
    try:
        df = pd.read_csv(file_path)
        if type(df) != pd.DataFrame:
            raise TypeError("The loaded data is not a DataFrame.")
    except Exception as e:
        raise TypeError("Failed to load the data: {}".format(e))
    
    # 점수 차이 계산 및 정렬
    df['score_difference'] = abs(df['쾌-불쾌'] - diary_score)
    df_sorted = df.sort_values('score_difference', ascending=True)
    
    # 가장 유사한 감정 추출
    closest_emotions = df_sorted['단어'].head(num_emotions).tolist()
    
    return closest_emotions

def extract_discomfort_score(text):
    """
    주어진 텍스트에서 불쾌 수치를 추출합니다.

    이 함수는 텍스트에서 "불쾌 수치 : X.X" 패턴을 찾아 X.X가 1.0에서 6.99 사이의 
    소수인 경우 해당 점수를 문자열로 반환합니다. 패턴을 찾지 못하면 None을 반환합니다.

    매개변수:
    text (str): 불쾌 수치를 포함한 입력 텍스트.

    반환 값:
    str: 불쾌 수치가 추출된 경우 그 값을 문자열로 반환하고, 찾지 못하면 None을 반환합니다.

    예제:
    >>> extract_discomfort_score("나는 오늘 배가 너무 고파서 밥을 먹었다. 그랬더니 지금 상당히 기분이 좋다. 내일도 맛있는 밥을 먹어야겠다.\n\n불쾌 수치 : 1.0")
    '1.0'
    >>> extract_discomfort_score("불쾌 수치 : 3.8")
    '3.8'
    """
    # 정규표현식 패턴 정의
    pattern = r'불쾌 수치\s*:\s*([1-6]\.\d{1,2})'
    match = re.search(pattern, text)
    if match:
        return float(match.group(1))
    else:
        return None

def text_to_score(text= "") -> int:
    client = OpenAI(api_key=prompt.get_api_key())
    

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"{prompt.get_score_prompt()}"},
            {"role": "user", "content": f"{text}"}
        ]
    )
    
    score = extract_discomfort_score(response.choices[0].message.content)
    return score

def json_to_message(content):
    messages =[
       {"role" : "system", "content" : prompt.get_sys_text()}
    ]
    

    data = json_to_dict()
       
    for idx, value in enumerate(data[data['content'][content]]):
        if idx% 2 == 0:
            messages.append({"role" : "user", "content" : value})
        elif idx % 2 == 1:
            messages.append({"role" : "assistant", "content" : value})
    
    return messages
   
       
       

def load_emotion(file_path: str) -> pd.DataFrame:
    """
    주어진 파일 경로에서 CSV 파일을 로드하여 데이터프레임으로 반환합니다.

    매개변수:
    file_path (str): CSV 파일의 경로.

    반환 값:
    pd.DataFrame: CSV 파일의 내용을 담고 있는 데이터프레임.
    """
    df = pd.read_csv(file_path)
    return df

def save_diary(id: str, content : str):
    content = content.replace('\r\n', '\n')
    data = {
        "content" : [content]
    }
    with open(f'diary/diary.json','w', encoding='utf-8', newline='\n') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    
def save_content(content: str):
    content = content.replace('\r\n', '\n')
    with open('diary/diary.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    if content in data['content'].keys():
        data[data['content'][content]] = [content]

    else:
        data['content'][content] = f"chat{len(data['content'])}"
        data[f"chat{len(data['content'])-1}"] = [content]

    with open('diary/diary.json', 'w', encoding='utf-8', newline='\n') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def cal_json_length(content):
    data = json_to_dict()
        
    content_length = len(data[data['content'][content]])
    return content_length

def extract_numbers_from_filenames(directory='diary/'):
    """
    지정된 디렉토리에서 'diary_*.json' 형식의 파일 이름에서 숫자를 추출하여 리스트로 반환합니다.
    :param directory: 디렉토리 경로
    :return: 숫자 리스트
    """
    # 숫자를 추출할 정규 표현식 패턴
    pattern = r"diary_(\d+)\.json"

    # 디렉토리 내의 파일 목록 가져오기
    filenames = os.listdir(directory)


    # 파일 이름에서 숫자 추출
    numbers = []
    for filename in filenames:
        match = re.match(pattern, filename)
        if match:
            # 숫자 부분 추출하여 정수로 변환 후 리스트에 추가
            number = int(match.group(1))
            numbers.append(number)

    return numbers
