"""
AI 디버깅 서비스 (프리미엄 전용).
사용자가 에러 메시지/코드를 붙여넣으면 Gemini AI가 원인 분석 + 해결책 제시.
"""

import json
import logging
import os

import google.generativeai as genai

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

DEBUG_SYSTEM_PROMPT = """당신은 전문 소프트웨어 디버거 AI입니다.
개발자가 제공한 에러 메시지와 코드를 분석하여 명확하고 실용적인 해결책을 제시합니다.

분석 원칙:
- 에러의 근본 원인(root cause)을 정확히 파악
- 단계별 해결 방법 제시
- 수정된 코드 예시 제공 (가능한 경우)
- 유사한 실수를 방지하는 팁 포함
- 관련 공식 문서 링크 제안

응답 형식 (반드시 JSON으로만 반환):
{
  "root_cause": "에러의 핵심 원인 (1-2문장)",
  "solution": "단계별 해결 방법",
  "code_fix": "수정된 코드 (없으면 빈 문자열)",
  "explanation": "상세 설명 (왜 이런 에러가 발생했는지, 어떻게 방지하는지)",
  "references": ["관련 문서나 Stack Overflow 링크 (실제 존재하는 링크만)"]
}
"""

REVIEW_SYSTEM_PROMPT = """당신은 시니어 소프트웨어 엔지니어 AI입니다.
제공된 코드를 버그, 성능, 보안, 가독성 관점에서 종합적으로 리뷰합니다.

리뷰 원칙:
- 잠재적 버그와 엣지 케이스 식별
- 성능 병목 및 최적화 기회 제안
- 보안 취약점 (SQL injection, XSS 등) 탐지
- 코드 가독성 및 유지보수성 개선 제안
- 언어/프레임워크 모범 사례(best practice) 적용 여부 확인

응답 형식 (반드시 JSON으로만 반환):
{
  "summary": "전체적인 코드 품질 요약 (1-2문장)",
  "score": 점수 (0-100 정수),
  "issues": [
    {
      "severity": "critical|high|medium|low",
      "category": "bug|performance|security|readability|best_practice",
      "description": "문제 설명",
      "suggestion": "개선 방법",
      "line_hint": "해당 코드 라인 또는 패턴 (선택사항)"
    }
  ],
  "positives": ["잘 작성된 부분 목록"],
  "improved_code": "리팩토링된 전체 코드 (짧은 코드인 경우만, 길면 빈 문자열)"
}
"""


def _get_model(system_instruction: str) -> "genai.GenerativeModel | None":
    """Gemini 모델 인스턴스를 반환합니다. API 키 미설정 시 None."""
    if not GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY not set. AI features unavailable.")
        return None
    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=system_instruction,
    )


def _extract_json(raw_text: str) -> dict:
    """Gemini 응답에서 JSON을 추출하고 파싱합니다."""
    text = raw_text.strip()
    if "```" in text:
        parts = text.split("```")
        for part in parts:
            stripped = part.strip()
            if stripped.startswith("json"):
                stripped = stripped[4:].strip()
            if stripped.startswith("{"):
                text = stripped
                break
    # 중괄호 기준으로 추출
    start = text.find("{")
    end = text.rfind("}") + 1
    if start != -1 and end > start:
        text = text[start:end]
    return json.loads(text)


async def analyze_error(
    error_message: str,
    code_snippet: str = "",
    language: str = "python",
) -> dict:
    """
    에러 분석 및 해결책 제시.

    Args:
        error_message: 발생한 에러 메시지 또는 스택 트레이스
        code_snippet: 에러가 발생한 코드 (선택사항)
        language: 프로그래밍 언어 (기본값: python)

    Returns:
        dict: {
            "root_cause": "에러 원인",
            "solution": "해결 방법",
            "code_fix": "수정된 코드",
            "explanation": "상세 설명",
            "references": ["관련 문서 링크"]
        }
    """
    model = _get_model(DEBUG_SYSTEM_PROMPT)

    if model is None:
        return {
            "root_cause": "AI 서비스를 사용할 수 없습니다. 관리자에게 문의하세요.",
            "solution": "",
            "code_fix": "",
            "explanation": "GEMINI_API_KEY가 설정되지 않았습니다.",
            "references": [],
        }

    prompt_parts = [f"언어: {language}\n\n에러 메시지:\n```\n{error_message}\n```"]
    if code_snippet.strip():
        prompt_parts.append(f"\n관련 코드:\n```{language}\n{code_snippet}\n```")
    prompt = "\n".join(prompt_parts) + "\n\n위 에러를 분석하여 JSON 형식으로 답변해주세요."

    try:
        response = await model.generate_content_async(prompt)
        result = _extract_json(response.text)
        logger.info("Error analysis complete: language=%s", language)
        return result
    except json.JSONDecodeError as exc:
        logger.error("Failed to parse Gemini response as JSON: %s", exc)
        return {
            "root_cause": "분석 결과를 파싱할 수 없습니다.",
            "solution": "다시 시도해주세요.",
            "code_fix": "",
            "explanation": str(exc),
            "references": [],
        }
    except Exception as exc:
        logger.error("Gemini API call failed in analyze_error: %s", exc, exc_info=True)
        return {
            "root_cause": "AI 분석 중 오류가 발생했습니다.",
            "solution": "잠시 후 다시 시도해주세요.",
            "code_fix": "",
            "explanation": str(exc),
            "references": [],
        }


async def review_code(code: str, language: str = "python") -> dict:
    """
    코드 리뷰 - 버그/성능/보안 이슈 분석.

    Args:
        code: 리뷰할 코드
        language: 프로그래밍 언어 (기본값: python)

    Returns:
        dict: {
            "summary": "전체 품질 요약",
            "score": 0-100,
            "issues": [{"severity", "category", "description", "suggestion", "line_hint"}],
            "positives": ["잘 작성된 부분"],
            "improved_code": "리팩토링된 코드"
        }
    """
    model = _get_model(REVIEW_SYSTEM_PROMPT)

    if model is None:
        return {
            "summary": "AI 서비스를 사용할 수 없습니다.",
            "score": None,
            "issues": [],
            "positives": [],
            "improved_code": "",
        }

    prompt = (
        f"언어: {language}\n\n"
        f"리뷰할 코드:\n```{language}\n{code}\n```\n\n"
        "위 코드를 종합적으로 리뷰하여 JSON 형식으로 답변해주세요."
    )

    try:
        response = await model.generate_content_async(prompt)
        result = _extract_json(response.text)
        logger.info("Code review complete: language=%s, length=%d", language, len(code))
        return result
    except json.JSONDecodeError as exc:
        logger.error("Failed to parse Gemini review response as JSON: %s", exc)
        return {
            "summary": "리뷰 결과를 파싱할 수 없습니다.",
            "score": None,
            "issues": [],
            "positives": [],
            "improved_code": "",
        }
    except Exception as exc:
        logger.error("Gemini API call failed in review_code: %s", exc, exc_info=True)
        return {
            "summary": "AI 리뷰 중 오류가 발생했습니다.",
            "score": None,
            "issues": [],
            "positives": [],
            "improved_code": "",
        }
