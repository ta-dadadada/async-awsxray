import os
from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core.async_context import AsyncContext

DAEMON_ADDRESS = os.getenv('DAEMON_ADDRESS', '127.0.0.1:2000')
xray_recorder.configure(
    service='test-fastapi',
    sampling=False,
    context_missing='LOG_ERROR',
#    plugins=('EC2Plugin', ),
    daemon_address=DAEMON_ADDRESS,
    dynamic_naming='*mysite.com*',
    context=AsyncContext(),
)

recorder = xray_recorder


def set_http_metadata(segment, request: Request, response: Response):
    for k, v in (
        ('method', request.method),
        ('client_ip', request.client.host),
        ('url', str(request.url).split('?')[0]),
        ('user_agent', request.headers.get('user-agent')),
        ('status', response.status_code),
    ):
        segment.put_http_meta(key=k, value=v)


def set_metadata(segment, request: Request):
    for key, value in request.query_params.items():
        segment.put_metadata(key=key, value=value)


class TracingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        async with recorder.in_segment_async(request.url.path) as segment:
            response = await call_next(request)
            set_http_metadata(segment, request, response)
            set_metadata(segment, request)
        return response
