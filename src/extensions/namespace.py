# coding=utf-8
import logging
from functools import wraps

from flask import has_app_context, current_app, request
from flask_restx import Namespace as OriginalNamespace, marshal, Mask
from flask_restx._http import HTTPStatus
from flask_restx.utils import merge, unpack

# noinspection PyUnresolvedReferences
import src.extensions.model

from src.extensions.response_wrapper import wrap_response

__author__ = 'ThucNC'
_logger = logging.getLogger(__name__)


class Namespace(OriginalNamespace):
    def marshal_with(self, fields, as_list=False, code=HTTPStatus.OK, description=None, **kwargs):
        '''
        A decorator specifying the fields to use for serialization.

        :param bool as_list: Indicate that the return type is a list (for the documentation)
        :param int code: Optionally give the expected HTTP response code if its different from 200

        '''
        def wrapper(func):
            doc = {
                'responses': {
                    code: (description, [fields]) if as_list else (description, fields)
                },
                '__mask__': kwargs.get('mask', True),  # Mask values can't be determined outside app context
            }
            func.__apidoc__ = merge(getattr(func, '__apidoc__', {}), doc)
            return marshal_with(fields, ordered=self.ordered, **kwargs)(func)
        return wrapper


class marshal_with(object):
    """A decorator that apply marshalling to the return values of your methods.
    """
    def __init__(self, fields, metadata=None, envelope=None, skip_none=False, mask=None, ordered=False):
        """
        :param fields: a dict of whose keys will make up the final
                       serialized response output
        :param envelope: optional key that will be used to envelop the serialized
                         response
        """
        self.fields = fields
        self.metadata = metadata
        self.envelope = envelope
        self.skip_none = skip_none
        self.ordered = ordered
        self.mask = Mask(mask, skip=True)

    def __call__(self, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            resp = f(*args, **kwargs)
            if isinstance(resp, tuple):
                data, code, headers = unpack(resp)
                return (
                    self.wrap_response_with_data(data, code), code, headers
                )
            else:
                return self.wrap_response_with_data(resp)
        return wrapper

    def wrap_response_with_data(self, resp, code=200):
        mask = self.mask
        if has_app_context():
            mask_header = current_app.config['RESTX_MASK_HEADER']
            mask = request.headers.get(mask_header) or mask
        if isinstance(resp, dict) and all(k in resp for k in ['metadata', 'data']):
            return wrap_response(marshal(resp['data'], self.fields, self.envelope, mask),
                                 metadata=marshal(resp['metadata'], self.metadata),
                                 http_code=code)
        else:
            return wrap_response(marshal(resp, self.fields, self.envelope, mask),
                                 http_code=code)
