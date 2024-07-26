from openai import OpenAI
from utils import api

class EmptyFieldError(Exception):
    """
    필드가 비어있을 경우 생기는 오류입니다.
    """
    
    def __init__(self, message):
        super().__init__(message)


def words_lst_to_str(words_lst:list) -> str:
    """
    단어 리스트를 쉼표로 구분된 문자열로 변환합니다.

    이 함수는 단어(문자열)로 이루어진 리스트를 받아, 각 단어를 쉼표와 공백으로 구분된 하나의 문자열로 연결하고 마지막의 쉼표와 공백은 제거됩니다.

    매개변수:
        words_lst (list): 각 문자열이 단어인 문자열 리스트입니다.

    반환 값:
        str: 리스트에 있는 단어들을 쉼표와 공백으로 구분한 하나의 문자열입니다.

    예시:
        >>> words_lst_to_str(['사과', '바나나', '체리'])
        '사과, 바나나, 체리'
    """
    if not words_lst:
        raise EmptyFieldError("word_list is Empty")
    
    words_prompt = ''
    for word in words_lst:
        words_prompt += word+', '
    words_prompt = words_prompt[:-2]
    return words_prompt


def words_str_prompting(words_prompt:str) -> str:
    
    if not words_prompt:
        raise EmptyFieldError("words_prompt is Empty")
    
    client = OpenAI(api_key=api.get_api_key())
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content" : f"{words_prompt} {api.get_image_prompt()}"}
        ]
    )
    
    return response.choices[0].message.content


def generate_image(prompt: str) -> str:
    """
    주어진 프롬프트를 기반으로 DALL-E 3 모델을 사용하여 이미지를 생성하고,
    생성된 이미지의 URL을 반환합니다.

    Args:
        prompt (str): 이미지 생성을 위한 텍스트 프롬프트.

    Returns:
        str: 생성된 이미지의 URL.
    """
    
    if not prompt:
        raise EmptyFieldError("prompt is Empty")
    
    client = OpenAI(api_key=api.get_api_key())

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    
    return response.data[0].url
    

