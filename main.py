from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from utils import process, validators, generate
from errors import exceptions

import asyncio
import json, time

app = FastAPI()

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인에서의 접근을 허용합니다. 필요에 따라 구체적인 도메인으로 제한하세요.
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드를 허용합니다. 필요에 따라 "GET", "POST" 등으로 제한하세요.
    allow_headers=["*"],  # 모든 HTTP 헤더를 허용합니다. 필요에 따라 제한할 수 있습니다.
)
    
class DiaryEntry(BaseModel):
    content: str

class ChatEntry(BaseModel):
    content : str
    chatting : str
    




@app.post("/api/ai/image")
async def generate_image(entry: DiaryEntry):
    content = entry.content.replace('\r\n','\n')
    #validators.validate_hexacode(entry.hexacode) 
    if validators.validate_diary_content(content) == False:
        content = "일기에 대한 내용이 없음"
        process.save_content(content)
        words = ''
        prompt = '일기에 대한 내용 없음'
        url = 'https://emolog.s3.ap-northeast-2.amazonaws.com/default/%E1%84%8B%E1%85%B5%E1%86%AF%E1%84%80%E1%85%B51000.png'
    else:
        process.save_content(content)
        words = generate.generate_words_list(content)
        prompt = generate.generate_image_prompt(words)
        url = await asyncio.to_thread(generate.generate_image_url,prompt)
        

    return {"summary": prompt, "words": words, "url": url}


@app.post("/api/ai/emotion")
async def generate_emotion(entry: DiaryEntry):
    content = entry.content.replace('\r\n','\n')
    if validators.validate_diary_content(content) == False:

        content = "일기에 대한 내용이 없음"
        diary_score = 3.5
   # validators.validate_diary_content(content)
    else:
        for _ in range(3):
            diary_score = process.text_to_score(content)
        
            if diary_score == None or not(1.00 <= diary_score <= 6.99):
                continue
            else:
                break
        else:
            raise exceptions.content_not_generate_score()
        
    num_emotions=30
    
    emotion_lst = process.extract_closest_emotions('utils/emotion.csv', diary_score, num_emotions=num_emotions)
    
    return {"emotion_list": emotion_lst,"emotion_num": num_emotions, "emotion_score": str(diary_score)}

'''
@app.post("/api/ai/diary")
async def create_diary(entry : DiaryEntry):
    
    validators.validate_empty_diary_id(entry.diary_id)
    #validators.validate_diary_content(entry.content)
    
    process.save_diary(entry.diary_id, entry.content)

    return {"diary_id" : f"diary_id가 {entry.diary_id}인 일기가 성공적으로 생성되었습니다."}
'''
    
    

@app.post("/api/ai/chat")
async def generate_chat(entry: ChatEntry):
    await asyncio.sleep(1)
    content = entry.content.replace('\r\n','\n')
    if validators.validate_diary_content(content) == False:
        content = "일기에 대한 내용이 없음"
   # validators.validate_exist_diary_id(entry.content)
   # process.save_content(entry.content)   
    
   # with open("diary/diary.json", 'r', encoding='utf-8') as file:
   ##     data = json.load(file)
   # if content not in data['content'].keys():

    chat_length = process.cal_json_length(content)
    
    if chat_length == 1:
        chat = generate.generate_chat(content, "False")
    else:
        chat = generate.generate_chat(content, entry.chatting)
    
    
    if chat[-1] == '#':
        return {"chat" : chat[:-1], "endpoint" : "True"}
    else:
        return {"chat" : chat, "endpoint" : "False"}
"""
@app.get("/api/ai/diary_list")
async def read_diary_list():
    lst = process.extract_numbers_from_filenames()
    return {"diary_list": lst}
"""

@app.post("/api/ai/read_diary")
async def read_diary(entry:DiaryEntry):
    content = entry.content.replace('\r\n', '\n')
    validators.validate_exist_diary_id(content)
    data = process.json_to_dict()
    return data[data['content'][content]]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
