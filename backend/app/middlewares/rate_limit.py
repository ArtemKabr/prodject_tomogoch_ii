# backend/app/middlewares/rate_limit.py — простой rate limit для API
"""
Простой in-memory rate limiter (MVP).
Ключ: user_id (если есть валидный JWT), иначе IP.
"""

from __future__ import annotations  # (я добавил)

import time  # (я добавил)
from collections import deque  # (я добавил)

from fastapi import Request  # (я добавил)
from starlette.middleware.base import BaseHTTPMiddleware  # (я добавил)
from starlette.responses import JSONResponse  # (я добавил)

from app.core.config import settings  # (я добавил)
from app.core.security import decode_token  # (я добавил)


class RateLimitMiddleware(BaseHTTPMiddleware):  # (я добавил)
    """Rate limit для чата (MVP, in-memory)."""  # (я добавил)

    def __init__(self, app) -> None:  # (я добавил)
        super().__init__(app)  # (я добавил)
        self._hits: dict[str, deque[float]] = {}  # (я добавил)

    def _get_key(self, request: Request) -> str:  # (я добавил)
        auth = request.headers.get("authorization") or ""  # (я добавил)
        if auth.lower().startswith("bearer "):  # (я добавил)
            token = auth.split(" ", 1)[1].strip()  # (я добавил)
            try:  # (я добавил)
                payload = decode_token(token)  # (я добавил)
                user_id = payload.get("sub")  # (я добавил)
                if user_id:  # (я добавил)
                    return f"user:{user_id}"  # (я добавил)
            except Exception:
                pass  # (я добавил)

        # сначала пробуем X-Forwarded-For  # (я добавил)
        xff = request.headers.get("x-forwarded-for")  # (я добавил)
        if xff:  # (я добавил)
            ip = xff.split(",")[0].strip()  # (я добавил)
            if ip:  # (я добавил)
                return f"ip:{ip}"  # (я добавил)

        ip = request.client.host if request.client else "unknown"  # (я добавил)
        return f"ip:{ip}"  # (я добавил)

    async def dispatch(self, request: Request, call_next):  # (я добавил)
        if not settings.rate_limit_enabled:  # (я добавил)
            return await call_next(request)  # (я добавил)

        path = request.url.path  # (я добавил)
        if path != "/api/v1/chat":  # (я добавил)
            return await call_next(request)  # (я добавил)

        key = self._get_key(request)  # (я добавил)
        now = time.time()  # (я добавил)

        window_s = int(settings.rate_limit_window_s)  # (я добавил)
        limit = int(settings.rate_limit_requests)  # (я добавил)

        q = self._hits.setdefault(key, deque())  # (я добавил)

        # выкидываем старые события  # (я добавил)
        border = now - window_s  # (я добавил)
        while q and q[0] < border:  # (я добавил)
            q.popleft()  # (я добавил)

        # если очередь пустая — чистим ключ (чтобы dict не рос бесконечно)  # (я добавил)
        if not q:  # (я добавил)
            self._hits.pop(key, None)  # (я добавил)
            q = self._hits.setdefault(key, deque())  # (я добавил)

        if len(q) >= limit:  # (я добавил)
            return JSONResponse(  # (я добавил)
                status_code=429,  # (я добавил)
                content={"detail": "Too Many Requests"},  # (я добавил)
            )  # (я добавил)

        q.append(now)  # (я добавил)
        return await call_next(request)  # (я добавил)
