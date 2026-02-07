"""
테스트용 샘플 파일
gaco 프로그램의 동작을 테스트하기 위한 파일입니다.
"""

def hello_world():
    """간단한 인사 함수"""
    print("Hello, World!")
    return "Hello"

def add_numbers(a, b):
    """두 숫자를 더하는 함수"""
    return a + b

def main():
    """메인 함수"""
    hello_world()
    result = add_numbers(5, 3)
    print(f"5 + 3 = {result}")

if __name__ == "__main__":
    main()
