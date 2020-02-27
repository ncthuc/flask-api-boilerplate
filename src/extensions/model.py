from collections import OrderedDict, MutableMapping

from flask_restx.model import RawModel
from jsonschema import Draft4Validator
from jsonschema.exceptions import ValidationError

from src.extensions.exceptions import HTTPException


def validate(self, data, resolver=None, format_checker=None):
    validator = Draft4Validator(self.__schema__, resolver=resolver, format_checker=format_checker)
    try:
        validator.validate(data)
    except ValidationError:
        raise HTTPException(code=400, message='Input payload validation failed',
                            errors=dict(self.format_error(e) for e in validator.iter_errors(data)))


RawModel.validate = validate

