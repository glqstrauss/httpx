import typing
from base64 import b64encode

from .models import AsyncRequest


class AuthBase:
    """
    Base class that all auth implementations derive from.
    """

    def __call__(self, request: AsyncRequest) -> AsyncRequest:
        raise NotImplementedError("Auth hooks must be callable.")  # pragma: nocover


class HTTPBasicAuth(AuthBase):
    def __init__(
        self, username: typing.Union[str, bytes], password: typing.Union[str, bytes]
    ) -> None:
        self.username = username
        self.password = password

    def __call__(self, request: AsyncRequest) -> AsyncRequest:
        request.headers["Authorization"] = self.build_auth_header()
        return request

    def build_auth_header(self) -> str:
        return build_basic_auth_header(self.username, self.password)


def build_basic_auth_header(
    username: typing.Union[str, bytes], password: typing.Union[str, bytes]
) -> str:
    if isinstance(username, str):
        username = username.encode("latin1")

    if isinstance(password, str):
        password = password.encode("latin1")

    userpass = b":".join((username, password))
    token = b64encode(userpass).decode().strip()
    return f"Basic {token}"
