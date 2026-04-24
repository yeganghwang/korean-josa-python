# Korean Josa (korean-josa-python)

[![PyPI version](https://badge.fury.io/py/korean-josa.svg)](https://badge.fury.io/py/korean-josa)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

한국어 단어의 마지막 글자에 따라 적절한 조사를 자동으로 선택하고 결합해 주는 파이썬 라이브러리입니다.

## 핵심 기능

- **지능형 조사 선택**: 사용자가 은, 는, 은/는 중 하나만 입력해도 앞 단어의 받침 유무에 맞춰 자동으로 교정합니다.
- **한글 및 숫자 지원**: 한글 유니코드 분석과 숫자를 읽었을 때의 받침 유무(예: 1->일, 3->삼)를 판별합니다.
- **'ㄹ' 받침 예외 처리**: '으로/로' 조사의 경우, 'ㄹ' 받침(예: 하늘, 칼, 1, 7, 8) 뒤에 '로'가 오도록 특수 로직을 적용합니다.
- **템플릿 포맷팅**: format() 함수를 통해 문장 전체의 조사를 한 번에 교정할 수 있습니다.
- **Zero-Dependency**: 외부 라이브러리 의존성 없이 파이썬 표준 라이브러리만 사용하여 가볍고 빠릅니다.

## 설치 방법

```bash
pip install korean-josa
```

## 사용 예시

### 1. 기본 사용법 (attach)

단어와 조사를 입력하면 적절한 형태를 결합하여 반환합니다.

```python
import josa

print(josa.attach("사과", "은"))  # 사과는
print(josa.attach("책", "는"))    # 책은
print(josa.attach("수박", "이"))  # 수박이
print(josa.attach("포도", "가"))  # 포도가
```

### 2. 숫자 지원

숫자로 끝나는 단어도 한글 발음에 맞춰 조사를 선택합니다.

```python
print(josa.attach("1", "은"))   # 1은 (일)
print(josa.attach("2", "은"))   # 2는 (이)
print(josa.attach("10", "이"))  # 10이 (영)
```

### 3. 'ㄹ' 받침 예외 처리

'으로/로' 조사는 'ㄹ' 받침일 때 '로'가 선택됩니다.

```python
print(josa.attach("하늘", "으로")) # 하늘로
print(josa.attach("칼", "으로"))   # 칼로
print(josa.attach("8", "으로"))    # 8로 (팔)
```

### 4. 템플릿 포맷팅 (format)

파이프(|) 기호를 사용하여 문장 내 여러 조사를 한꺼번에 처리할 수 있습니다.

```python
result = josa.format("{name|은} {item|를} 샀다", name="수박", item="빵")
print(result) # 수박은 빵을 샀다

result = josa.format("{name|아} 안녕? {target|이랑} 놀자", name="철수", target="영희")
print(result) # 철수야 안녕? 영희랑 놀자
```

## 지원하는 조사 범위

- 은/는, 이/가, 을/를, 과/와, 아/야
- 으로/로 (ㄹ 받침 예외 포함)
- 이랑/랑, 이나/나, 이야/야, 이나마/나마, 이라야/라야 등

## 라이선스

이 프로젝트는 [MIT 라이선스](LICENSE)를 따릅니다.
