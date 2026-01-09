from __future__ import annotations

from dotenv import load_dotenv
load_dotenv()

import os
import time
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI

PLAIN_TEXT_SYSTEM_PROMPT = """
Bạn là hệ thống rewrite nội dung tiếng Việt chuyên nghiệp.

NHIỆM VỤ:
- Viết lại HOÀN TOÀN nội dung được cung cấp
- Văn phong khác rõ rệt, tự nhiên như người viết
- GIỮ NGUYÊN Ý NGHĨA, không thêm ý mới

RÀNG BUỘC:
- KHÔNG dùng HTML, KHÔNG markdown
- Độ dài nội dung đầu ra phải xấp xỉ đầu vào (±15%)
- Không lặp câu, không văn phong AI
- Không quảng cáo lố
- Không kêu gọi hành động
- Không nhắc nguồn, website, bên thứ ba
- Không emoji

OUTPUT:
- Trả về DUY NHẤT nội dung đã rewrite
- Không giải thích, không ghi chú
""".strip()

DEFAULT_SYSTEM_PROMPT = """
Bạn là hệ thống rewrite nội dung chuyên nghiệp cho website App APK.

NHIỆM VỤ:
- Viết lại hoàn toàn nội dung được cung cấp
- Văn phong khác rõ rệt so với bản gốc
- Giữ nguyên cấu trúc HTML, thứ tự thẻ, số lượng thẻ
- KHÔNG thay đổi:
  + <p>, <h2>, <img>, thứ tự xuất hiện
  + Thuộc tính của thẻ <img> (src, srcset, alt, class, width, height, loading, decoding...)
- CHỈ được thay đổi nội dung chữ trong thẻ <p> và <h2>

YÊU CẦU NỘI DUNG:
- Giữ đúng ý nghĩa gốc, không thêm ý mới
- Không lặp câu, không paraphrase máy móc
- Văn phong tự nhiên, giống người viết thật
- Không quảng cáo lố
- Không nhắc đến nguồn, website, bên thứ ba
- Không kêu gọi tải xuống
- Không thêm link
- Không dùng emoji

RÀNG BUỘC KỸ THUẬT:
- Không thêm, không xóa thẻ HTML
- Không gộp hoặc tách đoạn
- Không đổi chữ hoa/thường của tiêu đề nếu không cần
- Không dịch ngôn ngữ (giữ nguyên tiếng gốc)

OUTPUT:
- Trả về DUY NHẤT HTML đã được rewrite
- Không giải thích, không ghi chú
- Trả về với ngôn ngữ tiếng Việt
""".strip()


@dataclass
class RewriteConfig:
    model: str = "gpt-4.1-mini"
    temperature: float = 0.7
    top_p: float = 0.9
    max_output_tokens: int = 2500
    system_prompt: str = DEFAULT_SYSTEM_PROMPT
    retries: int = 3
    retry_sleep_sec: float = 1.2


class GPTRewriter:
    """
    Usage:
        from gpt_rewriter import GPTRewriter, RewriteConfig
        rw = GPTRewriter(api_key="...", config=RewriteConfig())
        html2 = rw.rewrite_html(html1)
    """

    def __init__(self, api_key: Optional[str] = None, config: Optional[RewriteConfig] = None):
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Missing OPENAI_API_KEY. Pass api_key=... or set env OPENAI_API_KEY.")

        self.client = OpenAI(api_key=api_key)
        self.config = config or RewriteConfig()

    def rewrite_html(self, html_input: str) -> str:
        if not isinstance(html_input, str) or not html_input.strip():
            raise ValueError("html_input must be a non-empty string")

        user_input = f"ĐẦU VÀO:\n{html_input.strip()}\n\nĐẦU RA:\n"

        last_err: Optional[Exception] = None
        for attempt in range(1, self.config.retries + 1):
            try:
                res = self.client.responses.create(
                    model=self.config.model,
                    temperature=self.config.temperature,
                    top_p=self.config.top_p,
                    max_output_tokens=self.config.max_output_tokens,
                    input=[
                        {"role": "system", "content": self.config.system_prompt},
                        {"role": "user", "content": user_input},
                    ],
                )

                text = (res.output_text or "").strip()
                if not text:
                    raise RuntimeError("Empty output from model")

                # if "<p" not in text and "<h2" not in text:
                #     raise RuntimeError("Output doesn't look like HTML")

                return text

            except Exception as e:
                last_err = e
                if attempt < self.config.retries:
                    time.sleep(self.config.retry_sleep_sec * attempt)
                else:
                    raise RuntimeError(f"rewrite_html failed after {self.config.retries} retries: {e}") from e

        # unreachable
        raise RuntimeError(f"rewrite_html failed: {last_err}")

    def rewrite_text(self, text_input: str) -> str:
        if not isinstance(text_input, str) or not text_input.strip():
            raise ValueError("text_input must be a non-empty string")

        user_input = f"NỘI DUNG GỐC:\n{text_input.strip()}\n\nNỘI DUNG ĐÃ VIẾT LẠI:\n"

        last_err: Optional[Exception] = None
        for attempt in range(1, self.config.retries + 1):
            try:
                res = self.client.responses.create(
                    model=self.config.model,
                    temperature=self.config.temperature,
                    top_p=self.config.top_p,
                    max_output_tokens=self.config.max_output_tokens,
                    input=[
                        {"role": "system", "content": PLAIN_TEXT_SYSTEM_PROMPT},
                        {"role": "user", "content": user_input},
                    ],
                )

                text = (res.output_text or "").strip()
                if not text:
                    raise RuntimeError("Empty output from model")

                # sanity check: không được có HTML
                if "<" in text and ">" in text:
                    raise RuntimeError("Output contains HTML tags")

                return text

            except Exception as e:
                last_err = e
                if attempt < self.config.retries:
                    time.sleep(self.config.retry_sleep_sec * attempt)
                else:
                    raise RuntimeError(
                        f"rewrite_text failed after {self.config.retries} retries: {e}"
                    ) from e

        raise RuntimeError(f"rewrite_text failed: {last_err}")
