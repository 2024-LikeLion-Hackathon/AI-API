from fastapi import HTTPException

def content_not_exist():
    """일기의 내용이 존재하지 않을 때 발생하는 예외"""
    return HTTPException(
        status_code=400,
        detail={
            "message" : "해당 일기의 내용이 존재하지 않습니다.",
            "code": "AI-300"
        }
    )

def content_too_short_exception():
    """컨텐츠 길이가 너무 짧을 때 발생하는 예외"""
    return HTTPException(
        status_code=403,
        detail={
            "message": "해당 일기 내용의 길이가 짧아서 AI 생성할 수 없습니다.",
            "code": "AI-301"
        }
    )

def content_too_long_exception():
    """컨텐츠 길이가 너무 길 때 발생하는 예외"""
    return HTTPException(
        status_code=403,
        detail={
            "message": "해당 일기 내용의 길이가 1500자를 초과합니다.",
            "code": "AI-302"
        }
    )

def content_not_generate_prompt():
    """컨텐츠 내용이 아무 의미가 없을 때 발생하는 예외"""
    return HTTPException(
        status_code=400,
        detail={
            "message" : "해당 일기 내용으로 프롬프트를 생성할 수 없습니다.",
            "code" : "AI-303"
        }
    )

def hexacode_length_exception(hexacode:int):
    """헥사코드의 길이가 6이 아닐 때 발생하는 예외"""
    return HTTPException(
        status_code=403,
        detail={
            "message" : f"헥사코드 : {hexacode}의 길이가 6이 아닙니다.",
            "code" : "AI-304",
        }
    )
 
def hexacode_code_exception(hexacode:int):
    """헥사코드에서 0 ~ f가 아닌 문자가 있을 때 발생하는 예외"""
    return HTTPException(
        status_code=403,
        detail={
            "message" : f"헥사코드 : {hexacode}에 0 ~ f 이외의 문자가 포함되어 있습니다.",
            "code" : "AI-305",
        }
    )
    
def content_not_generate_score():
    """컨텐츠 내용으로 점수를 생성하지 못했습니다."""
    return HTTPException(
        status_code=400,
        detail={
            "message" : "해당 일기 내용으로 점수를 생성하지 못했습니다.",
            "code" : "AI-306"
        }
    )
    
def diary_alreay_exist():
    """해당 일기가 이미 존재할 때 발생하는 예외"""
    return HTTPException(
        status_code=400,
        detail={
            "message" : "해당 일기가 이미 존재합니다.",
            "code" : "Chat-401"
        }
    )

def diary_not_exist():
    """해당 일기가 존재하지 않을 때 발생하는 예외"""
    raise HTTPException(
        status_code=400,
        detail={
            "message" : "해당 일기가 존재하지 않습니다.",
            "code" : "Chat-402"
        }
    )