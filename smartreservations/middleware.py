import logging
import re
from typing import Optional

logger = logging.getLogger(__name__)

class UserActivityLoggingMiddleware:
    """
    Persists basic request/response metadata for authenticated users.
    """

    SENSITIVE_METHODS = {'POST', 'PUT', 'PATCH', 'DELETE'}
    PATH_PREFIX_BLACKLIST = (
        '/static/',
        '/favicon.ico',
        '/api/me/activity/'
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        body_snapshot = ''
        if request.method in self.SENSITIVE_METHODS:
            body_snapshot = self._extract_body(request)

        response = self.get_response(request)
        self._persist_activity(request, response, body_snapshot)
        return response

    def _extract_body(self, request) -> str:
        try:
            raw_body = request.body.decode('utf-8', errors='ignore')
        except Exception:
            return ''

        raw_body = raw_body.strip()
        if len(raw_body) > 2000:
            raw_body = f'{raw_body[:2000]}…'
        return raw_body

    def _persist_activity(self, request, response, body_snapshot: str) -> None:
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return

        path = request.path or ''
        if any(path.startswith(prefix) for prefix in self.PATH_PREFIX_BLACKLIST):
            return

        from users.models import UserActivity  # Local import to avoid circular dependencies

        try:
            UserActivity.objects.create(
                user=user,
                method=request.method,
                path=path[:512],
                status_code=getattr(response, 'status_code', 0) or 0,
                ip_address=self._get_ip(request),
                user_agent=(request.META.get('HTTP_USER_AGENT') or '')[:1024],
                query_params=(request.META.get('QUERY_STRING') or '')[:1024],
                payload=body_snapshot,
            )
        except Exception as e:
            logger.exception(f"UserActivity log failed for user={user}: {e}")
            pass

    @staticmethod
    def _get_ip(request) -> Optional[str]:
        forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        if forwarded:
            ip = forwarded.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '')

        if ':' in ip:
            ip = re.sub(r':\d+$', '', ip)

        return ip or None