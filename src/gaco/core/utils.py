"""
gaco의 유틸리티 함수들
"""
import sys

def safe_decode(binary_data: bytes) -> str:
    """
    바이너리 데이터를 안전하게 디코딩 (UTF-8 -> CP949 -> Replace 순)

    Args:
        binary_data: 디코딩할 바이트 데이터

    Returns:
        str: 디코딩된 문자열
    """
    if not isinstance(binary_data, bytes):
        return str(binary_data)

    # 시도해볼 인코딩 순서
    for encoding in ['utf-8', 'cp949']:
        try:
            return binary_data.decode(encoding)
        except UnicodeDecodeError:
            continue

    # 모든 시도가 실패하면 깨지는 문자를 '?'로 치환해서라도 반환
    return binary_data.decode('utf-8', errors='replace')


def print_error(message: str) -> None:
    """
    사용자 친화적인 에러 메시지를 출력

    Args:
        message: 출력할 에러 메시지
    """
    print(f"\n{message}\n", file=sys.stderr)
