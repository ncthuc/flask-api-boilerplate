from src.extensions.reqparse import RequestParser


class RequestHelper:
    pagination_params = RequestParser(bundle_errors=True)
    pagination_params.add_argument('page', type=int, help='Page number, starting from 1', required=False, default=1,
                                   location='args')
    pagination_params.add_argument('pageSize', type=int, help='Page size', required=False, default=10,
                                   location='args')
