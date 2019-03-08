from src.extensions.reqparse import RequestParser


class RequestHelper:
    @staticmethod
    def add_pagination_params(args):
        args.add_argument('page', type=int, help='Page number, starting from 1',
                          required=False, default=1, location='args')
        args.add_argument('pageSize', type=int, help='Page size',
                          required=False, default=10, location='args')
        return args

    @staticmethod
    def get_list_user_arguments():
        args = RequestParser(bundle_errors=True)
        RequestHelper.add_pagination_params(args)
        return args
