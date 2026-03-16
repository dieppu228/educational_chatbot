"""
Query Rewriter Handler
Rewrites short queries into multiple detailed queries with difficulty-based enrichment
"""

import json
import google.generativeai as genai

from config import settings


class QueryRewriter:
    """
    Rewrites user queries into multiple detailed queries for better retrieval.

    Difficulty levels:
        - Basic (cơ bản)
        - Intermediate (trung bình)
        - Advanced (nâng cao)
    
    Example:
        Input: "mã hóa dữ liệu"
        Output: [
            "Khái niệm mã hóa dữ liệu, mục đích và ví dụ cơ bản như mã Caesar, mã thay thế",
            "Nguyên lý hoạt động của mã hóa đối xứng và bất đối xứng, so sánh AES và RSA",
            "Thiết kế và triển khai hệ thống mã hóa trong ứng dụng thực tế, quản lý khóa và bảo mật nâng cao"
        ]
    """

    def __init__(self):
        """Initialize QueryRewriter with Gemini API"""
        self.model_name = settings.LLM_MODEL
        self.temperature = 0.3  # Focused, less creative

        # Initialize Gemini
        if settings.GENAI_API_KEY:
            genai.configure(api_key=settings.GENAI_API_KEY)
        else:
            raise ValueError("GENAI_API_KEY not set in environment")

    def handle(self, query: str) -> str:
        """
        Rewrite query into 3 difficulty-based detailed queries.

        Args:
            query: Original user query (e.g., "mã hóa dữ liệu")

        Returns:
            JSON string containing rewritten queries
        """
        try:
            prompt = self._build_rewrite_prompt(query)

            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.temperature,
                )
            )

            response_text = response.text.strip()
            result = self._parse_response(response_text)

            return json.dumps(result, ensure_ascii=False, indent=2)

        except Exception:
            return self._fallback_rewrite(query)

    def _build_rewrite_prompt(self, query: str) -> str:
        """Build prompt for difficulty-based query rewriting"""
        return f"""Bạn là chuyên gia tìm kiếm tài liệu kỹ thuật.

        Hãy viết lại câu hỏi của người dùng thành 3 truy vấn ngắn, dạng từ khóa, với độ khó tăng dần để phục vụ hệ thống truy xuất tài liệu.

        Câu hỏi gốc: "{query}"

        Quy tắc:
        1. Tạo đúng 3 truy vấn:
        - Cơ bản: định nghĩa, thuật ngữ, khái niệm nền tảng
        - Trung bình: thuật toán, phương pháp, phân loại, thành phần hệ thống
        - Nâng cao: kiến trúc hệ thống, triển khai thực tế, hiệu năng, bảo mật, tối ưu
        2. Mỗi truy vấn phải:
        - Dài 10–15 token
        - Dạng từ khóa, không viết thành câu hoàn chỉnh
        - Ưu tiên thuật ngữ kỹ thuật, tránh từ chung chung
        3. Hạn chế trùng token giữa các truy vấn (dưới 50%)
        4. Mỗi truy vấn phải hướng tới một nhóm tài liệu kỹ thuật khác nhau

        Trả về JSON duy nhất:
        {{
        "original_query": "{query}",
        "queries": [
            "từ khóa cơ bản",
            "từ khóa trung bình",
            "từ khóa nâng cao"
        ]
        }}
        """


    def _parse_response(self, response_text: str) -> dict:
        """Parse and validate response from Gemini"""
        try:
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]

            data = json.loads(response_text.strip())
            queries = data.get("queries", [])

            return {
                "original_query": data.get("original_query", ""),
                "queries": queries if isinstance(queries, list) else [],
                "count": len(queries) if isinstance(queries, list) else 0
            }

        except json.JSONDecodeError:
            return self._fallback_parse(response_text)

    def _fallback_parse(self, response_text: str) -> dict:
        """Fallback parsing if JSON extraction fails"""
        sentences = [s.strip() for s in response_text.split(".") if s.strip()]
        queries = sentences[:3] if len(sentences) >= 3 else sentences

        return {
            "original_query": "unknown",
            "queries": queries,
            "count": len(queries)
        }

    def _fallback_rewrite(self, query: str) -> str:
        """Fallback rewrite if API call fails"""
        return json.dumps({
            "original_query": query,
            "queries": [
                f"{query} - khái niệm và ví dụ cơ bản",
                f"{query} - nguyên lý hoạt động và phân loại",
                f"{query} - triển khai thực tế và tối ưu nâng cao"
            ],
            "count": 3
        }, ensure_ascii=False, indent=2)


__all__ = ["QueryRewriter"]
