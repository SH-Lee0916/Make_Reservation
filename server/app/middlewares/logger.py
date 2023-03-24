import logging
import time
import json
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import Message

# For typing
from typing import Callable
from fastapi import FastAPI, Request, Response


class MiddleLogger(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, logger: logging.Logger) -> None:
        self._logger = logger
        super().__init__(app)

    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id: str = str(uuid4())

        logging_info = {"X-API-REQUEST-ID": request_id}

        await self.set_body(request)
        response, response_info = await self._log_response(call_next, request, request_id)

        request_info = await self._log_request(request)

        logging_info["request"] = request_info
        logging_info["response"] = response_info

        self._logger.info(logging_info)

        return response
    

    async def set_body(self, request: Request):
        receive_ = await request._receive()

        async def recieve() -> Message:
            return receive_
        
        request._receive = recieve

    
    async def _log_response(self, call_next: Callable, request: Request, request_id: str) -> Response:
        start_time = time.perf_counter()
        response: Response = await self._execute_request(call_next, request, request_id)
        end_time = time.perf_counter()

        overall_status = "SUCCESS" if response.status_code < 400 else "FAIL"
        excution_time = end_time - start_time

        response_info = {
            "status": overall_status,
            "status_code": response.status_code,
            "excution_time": excution_time
        }

        response_body = [section async for section in response.__dict__["body_iterator"]]
        response.__setattr__("body_interator", AsyncIteratorWrapper(response_body))

        try:
            response_body = json.loads(response_body[0].decode())
        except:
            response_body = str(response_body)

        response_info["body"] = response_body

        return response, response_info


    async def _execute_request(self, call_next: Callable, request: Request, request_id: str) -> Response:
        try:
            response: Response = await call_next(request)
            response.headers["X-API-REQUEST-ID"] = request_id
            
            return response

        except Exception as e:
            self._logger.exception(
                {
                    "path": request.url.path,
                    "method": request.method,
                    "resone": e
                }
            )


    async def _log_request(self, request: Request) -> str:
        path = request.url.path
        if request.query_params:
            path += f"?{request.query_params}"
        
        request_info = {
            "method": request.method,
            "path": path,
            "ip": request.client.host
        }

        try:
            body = await request.json()
            request_info["body"] = body
        except:
            body = None

        return request_info


class AsyncIteratorWrapper:
    """The following is a utility class that transforms a
        regular iterable to an asynchronous one.

        link: https://www.python.org/dev/peps/pep-0492/#example-2
    """

    def __init__(self, obj):
        self._it = iter(obj)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            value = next(self._it)
        except StopIteration:
            raise StopAsyncIteration
        return value