from functools import cached_property

from flask import request
from flask_restful import Resource as FlaskResource

from .request import RequestParams


class Resource(FlaskResource):

    @cached_property
    def request(self):
        return request

    @cached_property
    def params(self):
        return RequestParams(self.request)
