"""
gaco의 커스텀 예외 클래스들
"""

class GacoError(Exception):
    """gaco 프로그램의 커스텀 예외 클래스"""
    pass


class GitNotFoundError(GacoError):
    """Git 저장소를 찾을 수 없을 때 발생하는 예외"""
    pass


class NoStagedChangesError(GacoError):
    """Staged된 변경사항이 없을 때 발생하는 예외"""
    pass


class APIKeyError(GacoError):
    """API 키 관련 오류가 발생했을 때의 예외"""
    pass


class GeminiFileNotFoundError(GacoError):
    """docs/config/GEMINI.md 파일을 찾을 수 없을 때 발생하는 예외"""
    pass
