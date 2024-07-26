import pandas as pd

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

def extract_similar_emotion(file_path: str, diary_score: float, threshold: float = 0.3) -> list:
    """
    주어진 파일 경로에서 CSV 파일을 로드하여 불쾌 수치가 유사한 감정을 추출합니다.

    매개변수:
    file_path (str): CSV 파일의 경로.
    diary_score (float): 비교할 일기의 불쾌 수치.
    threshold (float, optional): 일기와 유사한 불쾌 수치의 감정을 추출하는 임계값. 기본값은 0.3입니다.

    반환 값:
    list: 유사한 불쾌 수치의 감정 단어 리스트.

    예외:
    TypeError: 데이터프레임을 로드하지 못한 경우 발생합니다.
    """
    df = pd.read_csv(file_path)
    
    if type(df) != pd.DataFrame:
        raise TypeError("The loaded data is not a DataFrame.")
    
    emotion_lst = []
    for idx, score in enumerate(df['쾌-불쾌']):
        if abs(score - diary_score) <= threshold:
            emotion_lst.append(df['단어'][idx])
    
    return emotion_lst
