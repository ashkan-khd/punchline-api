from flask import Request


class RequestParams:
    def __init__(self, request: Request):
        self.__request = request

    def as_list(self) -> "RequestParamsAsList":
        return RequestParamsAsList(self.__request)

    def __getattr__(self, item) -> str:
        return self.__request.args.get(item, "").strip()


class RequestParamsAsList:
    def __init__(self, request: Request):
        self.__request = request

    def __getattr__(self, item) -> list:
        return [value.strip() for value in self.__request.args.getlist(item)]
