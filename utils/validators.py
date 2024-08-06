from errors import exceptions
from utils import generate

import os, json

def validate_diary_content(content: str):
    """일기 내용의 유효성 검사 및 예외 발생"""
    if content == None or content == "":
        raise exceptions.content_not_exist()

    if len(content) <= 5:
        raise exceptions.content_too_short_exception()

    if len(content) > 1500:
        raise exceptions.content_too_long_exception()
    
    if generate.generate_validate_content(content) == "False":
        return False
    
    
    
def validate_hexacode(hexacode: str):
    if len(hexacode) != 6:
        raise exceptions.hexacode_length_exception(hexacode)
    
    for char in hexacode:
        if char not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']:
            raise exceptions.hexacode_code_exception(hexacode)
    
def validate_empty_diary_content(content:str):
    """해당 일기가 이미 존재할 때 발생하는 예외"""
    filename = f"diary/diary.json"

    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)

    if content in list(data['content'].keys()):
        raise exceptions.diary_alreay_exist()
    
def validate_exist_diary_id(content:str):
    """해당 일기가 존재하지 않을 때 발생하는 예외"""
    filename = f"diary/diary.json"

    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)

    if content not in list(data['content'].keys()):
        raise exceptions.diary_not_exist()
