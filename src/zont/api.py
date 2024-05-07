from __future__ import annotations

import requests
import typing as t


__all__ = [
    "API",
    "NotAuthorizedError",
    "UnexpectedResponse",
    "ZontError",
]


class ZontError(Exception):
    def __init__(self, code: str, descr: str | list[str]) -> None:
        self.code = code
        self.description = descr if isinstance(descr, str) else "\n".join(descr)
        super().__init__(f"{self.code}: {self.description}")


class NotAuthorizedError(ZontError):
    def __init__(self) -> None:
        super("not_authorized", "Client has not been authorized")


class UnexpectedResponse(ZontError):
    def __init__(self) -> None:
        super("invalid_response", "Unexpected or malformed response")


class API:
    URL: str = "https://lk.zont-online.ru/api"

    class Method:
        def __init__(self, name: str, owner: API) -> None:
            self.name = name
            self.owner = owner

        def __call__(self, **kwargs: t.Any) -> t.Any:
            return self.owner.request(self.name, kwargs)

    def __init__(self, client_id: str, token: str | None = None) -> None:
        self.headers = {"Content-Type": "application/json", "X-ZONT-Client": client_id}
        self.token = token
        if self.token:
            self.headers["X-ZONT-Token"] = self.token
        self.session = requests.Session()

    @staticmethod
    def check_result(r: t.Any) -> None:
        if not isinstance(r, dict) or "ok" not in r:
            raise UnexpectedResponse()
        if not r["ok"]:
            raise ZontError(r.get("error", "unknown"), r.get("error_ui", "unknown"))

    def authenticate(self, login: str, password: str, app_name: str | None = None) -> None:
        r = self.session.post(
            url=f"{self.URL}/get_authtoken",
            headers=self.headers,
            auth=(login, password),
            json={"client_name": app_name or "pyzont"},
        )
        r.raise_for_status()
        data = r.json()
        self.check_result(data)
        self.token = data["token"]
        self.headers["X-ZONT-Token"] = self.token

    def request(self, method: str, data: dict[str, t.Any]) -> t.Any:
        if not self.token:
            raise NotAuthorizedError()
        r = self.session.post(
            url=f"{self.URL}/{method}",
            json=data,
            headers=self.headers,
        )
        r.raise_for_status()
        data = r.json()
        self.check_result(data)
        return data

    def __getattr__(self, method_name: str) -> t.Any:
        return self.Method(method_name, self)
