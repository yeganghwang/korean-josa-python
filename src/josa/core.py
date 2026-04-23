import re
from typing import Dict, Tuple, Optional

# 조사 쌍 매핑 (입력된 조사가 어떤 쌍에 속하는지 판별하기 위함)
JOSA_PAIRS: Dict[str, Tuple[str, str]] = {
    "은": ("은", "는"), "는": ("은", "는"),
    "이": ("이", "가"), "가": ("이", "가"),
    "을": ("을", "를"), "를": ("을", "를"),
    "과": ("과", "와"), "와": ("과", "와"),
    "으로": ("으로", "로"), "로": ("으로", "로"),
    "아": ("아", "야"), "야": ("아", "야"),
    "이랑": ("이랑", "랑"), "랑": ("이랑", "랑"),
    "이나": ("이나", "나"), "나": ("이나", "나"),
    "이야": ("이야", "야"),
    "이나마": ("이나마", "나마"), "나마": ("이나마", "나마"),
    "이라야": ("이라야", "라야"), "라야": ("이라야", "라야"),
}

# 숫자 받침 매핑 (0~9)
NUMBER_HAS_BATCHIM: Dict[str, bool] = {
    "0": True, "1": True, "2": False, "3": True, "4": False,
    "5": False, "6": True, "7": True, "8": True, "9": False
}

def has_batchim(text: str) -> Optional[bool]:
    """단어의 마지막 글자에 받침이 있는지 판별합니다."""
    if not text:
        return None
    
    last_char = text[-1]
    
    # 한글 판별
    if '가' <= last_char <= '힣':
        # (ord(char) - 0xAC00) % 28 == 0 이면 받침 없음
        return (ord(last_char) - 0xAC00) % 28 != 0
    
    # 숫자 판별
    if last_char.isdigit():
        return NUMBER_HAS_BATCHIM.get(last_char, False)
    
    # 그 외 (영어 등) - 기본값으로 받침 없음 처리 (확장 가능)
    return False

def is_rieul_batchim(text: str) -> bool:
    """단어의 마지막 글자가 'ㄹ' 받침인지 판별합니다."""
    if not text:
        return False
    
    last_char = text[-1]
    
    # 한글 'ㄹ' 받침 (종성 인덱스 8)
    if '가' <= last_char <= '힣':
        return (ord(last_char) - 0xAC00) % 28 == 8
    
    # 숫자의 경우 '1', '7', '8'이 'ㄹ'로 끝남 (일, 칠, 팔)
    if last_char in ('1', '7', '8'):
        return True
        
    return False

def get_josa(word: str, josa: str) -> str:
    """단어에 맞는 적절한 조사를 선택합니다."""
    # 정규화: (은)는, 은/는 등을 단일 형태로 변환
    clean_josa = re.sub(r'[^가-힣]', '', josa)
    
    # 1. 정확한 매칭 우선 확인
    if clean_josa in JOSA_PAIRS:
        pair = JOSA_PAIRS[clean_josa]
    else:
        # 2. 부분 매칭 확인 (가장 긴 매칭을 우선함 - 예: '이랑' > '이')
        sorted_pairs = sorted(JOSA_PAIRS.items(), key=lambda x: len(x[0]), reverse=True)
        pair = None
        for k, v in sorted_pairs:
            if k in josa or josa in k:
                pair = v
                break
            
    if not pair:
        return josa # 매핑되지 않은 조사는 그대로 반환

    batchim = has_batchim(word)
    
    # '으로/로' 예외 처리: ㄹ 받침이 있으면 '로' 선택
    if pair == ("으로", "로"):
        if batchim and not is_rieul_batchim(word):
            return "으로"
        return "로"
    
    # 일반적인 경우: 받침 있으면 앞의 것(은/이/을), 없으면 뒤의 것(는/가/를)
    return pair[0] if batchim else pair[1]

def attach(word: str, josa: str) -> str:
    """단어에 적절한 조사를 붙여 반환합니다."""
    return f"{word}{get_josa(word, josa)}"

def format(template: str, **kwargs) -> str:
    """템플릿 문자열의 조사를 자동으로 교정하여 반환합니다.
    예: format("{name|은} {item|를} 샀다", name="수박", item="빵")
    """
    def replace_func(match):
        full_match = match.group(0)
        key = match.group(1)
        josa = match.group(2)
        
        if key in kwargs:
            value = str(kwargs[key])
            return attach(value, josa)
        return full_match

    # {key|josa} 패턴 매칭
    pattern = r"\{([^|{}]+)\|([^|{}]+)\}"
    return re.sub(pattern, replace_func, template)
