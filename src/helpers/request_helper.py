# from src.extensions.reqparse import RequestParser
from flask import request
from flask_restplus.reqparse import RequestParser


class RequestHelper:
    @staticmethod
    def add_pagination_params():
        args = RequestParser(bundle_errors=True)

        args.add_argument('page', type=int, help='Page number, starting from 1',
                          required=False, default=1, location='args')
        args.add_argument('pageSize', type=int, help='Page size',
                          required=False, default=10, location='args')
        return args

    @staticmethod
    def get_remote_ip(req=None):
        if not req:
            req = request
        ip: str = req.remote_addr
        if ip in ['127.0.0.1', 'localhost']:
            if req.headers.get('X-Real-Ip'):
                ip = req.headers.get('X-Real-Ip')
            if ip.startswith("10."):
                if req.headers.get('X-Forwarded-For'):
                    ip = req.headers.get('X-Forwarded-For')
                    if ip and ", " in ip:
                        ip = ip.split(", ")[0]
        return ip

    @staticmethod
    def get_user_agent(req=None):
        if not req:
            req = request
        return req.headers.get('User-Agent')

