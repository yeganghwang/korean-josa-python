import unittest
import sys
import os

# 테스트를 위해 src 경로 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import josa

class TestJosa(unittest.TestCase):
    def test_basic_attach(self):
        self.assertEqual(josa.attach("사과", "은"), "사과는")
        self.assertEqual(josa.attach("책", "는"), "책은")
        self.assertEqual(josa.attach("수박", "이"), "수박이")
        self.assertEqual(josa.attach("포도", "가"), "포도가")
        self.assertEqual(josa.attach("당신", "라면"), "당신이라면")
        self.assertEqual(josa.attach("그것", "면"), "그것이면")

    def test_number_attach(self):
        self.assertEqual(josa.attach("1", "은"), "1은") # 일
        self.assertEqual(josa.attach("2", "은"), "2는") # 이
        self.assertEqual(josa.attach("3", "이"), "3이") # 삼
        self.assertEqual(josa.attach("4", "가"), "4가") # 사
        self.assertEqual(josa.attach("10", "은"), "10은") # 영(받침있음)

    def test_rieul_exception(self):
        # '으로/로'는 'ㄹ' 받침일 때 '로'를 선택해야 함
        self.assertEqual(josa.attach("하늘", "으로"), "하늘로")
        self.assertEqual(josa.attach("칼", "로"), "칼로")
        self.assertEqual(josa.attach("집", "으로"), "집으로")
        self.assertEqual(josa.attach("물", "로"), "물로")
        # 숫자 7(칠), 8(팔) 예외
        self.assertEqual(josa.attach("7", "으로"), "7로")
        self.assertEqual(josa.attach("8", "로"), "8로")
        self.assertEqual(josa.attach("1", "으로"), "1로") # 일 -> 일로 (ㄹ받침)

    def test_format_function(self):
        result = josa.format("{name|은} {item|를} 샀다", name="수박", item="빵")
        self.assertEqual(result, "수박은 빵을 샀다")
        
        result = josa.format("{name|야} 안녕? {target|이랑} 놀자", name="철수", target="영희")
        self.assertEqual(result, "철수야 안녕? 영희랑 놀자")


        result = josa.format("{a|이는} {b|가} 없다는 {c|를} {d|이와} {e|이가} 모두 알고 있습니다.", 
                             a="희선", b="아버지", c="사실", d="기철", e="기영")
        self.assertEqual(result, "희선이는 아버지가 없다는 사실을 기철이와 기영이가 모두 알고 있습니다.")

        
        result = josa.format("{val|은} {val|이} 된다", val=1)
        self.assertEqual(result, "1은 1이 된다")

    def test_various_josa_forms(self):
        # (은)는, 은/는 등 다양한 입력 처리
        self.assertEqual(josa.attach("사과", "은/는"), "사과는")
        self.assertEqual(josa.attach("책", "(은)는"), "책은")

if __name__ == '__main__':
    unittest.main()
