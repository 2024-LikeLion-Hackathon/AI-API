import re

from openai import OpenAI
from utils import prompt



class InputError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

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
    if text == "":
        raise InputError("text is None!!")
    
    client = OpenAI(api_key=prompt.get_api_key())
    
    for __ in range(3):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"{prompt.get_score_prompt()}"},
                {"role": "user", "content": f"{text}"}
            ]
        )
        
        score = extract_discomfort_score(response.choices[0].message.content)
        if score == None:
            continue
        elif not (1.00 <= score <= 6.99):
            continue 
        else:
            return score
    else:
        raise InputError("textError")

    