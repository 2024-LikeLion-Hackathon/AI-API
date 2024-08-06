from openai import OpenAI
from utils import prompt, process
from PIL import Image
from io import BytesIO

import requests, json



def download_image(url, save_path):
    # URL에서 이미지 데이터 가져오기
    response = requests.get(url)
    response.raise_for_status()  # HTTP 에러가 발생했는지 확인

    # 이미지 데이터를 메모리로 불러오기
    img_data = BytesIO(response.content)
    img = Image.open(img_data)

    # 이미지 저장
    img.save(save_path)

def generate_image_url(prompts) -> str:
    """
    주어진 프롬프트를 기반으로 DALL-E 3 모델을 사용하여 이미지를 생성하고,
    생성된 이미지의 URL을 반환합니다.

    Args:
        prompt (str): 이미지 생성을 위한 텍스트 프롬프트.

    Returns:
        str: 생성된 이미지의 URL.
    """
    
    client = OpenAI(api_key=prompt.get_api_key())

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content" : f"{prompts}\n\n 다음 내용을 영어로 번역해줘"}
        ]
    )

    translated_prompt = response.choices[0].message.content


    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt.get_image_url_prompt(translated_prompt),
        size="1024x1024",
        quality="standard",
        n=1,
    )
    
    url = response.data[0].url
   # download_image(url,f"images/{prompts}.jpg")
    

    return url

def generate_image_prompt(words_prompt:str) -> str:
    """단어들을 이용해 이미지 프롬프트 생성하고 프롬프트를 반환합니다."""
    client = OpenAI(api_key=prompt.get_api_key())
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content" : f"{words_prompt} {prompt.get_image_prompt()}"}
        ]
    )
    
    return response.choices[0].message.content

def generate_words_list(text:str):
    """일기내용에서 핵심 단어 리스트를 추출합니다."""
    
    client = OpenAI(api_key=prompt.get_api_key())

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content" : f"일기에서 핵심단어(물체 또는 행동)를 일기의 길이에 따라서 30자 마다 1단어씩 추가하여 최소 3개 ~ 최대 5개 정도 출력해줘\n 예를 들면, 햇살 가득한 공원, 친구들과 테니스를 즐기던 우리는 산책을 하며 차를 마신다. 웃음소리가 가득한 행복한 순간이다. 단어들 : [테니스, 동료, 산책, 차]\n {text}\n\n위의 내용은 일기이다. 위의 예시를 바탕으로 일기에 대해 다른말은 하지말고 예시처럼 단어들만 출력해줘. \n 단어들 : "}
        ]
    )
    return response.choices[0].message.content
        
def generate_validate_content(text:str):
    
    client = OpenAI(api_key=prompt.get_api_key())
    
    response = client.chat.completions.create(
        temperature=0.1,
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content" : f"{text}\n{prompt.get_validate_content_prompt()}"}
        ]
    )
    
    return response.choices[0].message.content

def generate_chat(content, chatting):
    
    messages = process.json_to_message(content)
    if chatting != False:
        messages.append({"role" : "user", "content" : chatting})
    
    
    client = OpenAI(api_key=prompt.get_api_key())
    response = client.chat.completions.create(
        temperature=0.1,
        model="gpt-4o-mini",
        messages=messages
    )
    
    # 생성된 답변 json에 추가하기
    data = process.json_to_dict()
    if chatting != "False":
        data[data['content'][content]].append(chatting)
        
    data[data['content'][content]].append(response.choices[0].message.content)
    
    with open(f"diary/diary.json", 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    
    return response.choices[0].message.content
    
