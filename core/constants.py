import os
from enum import Enum

ROOT_WORKING_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_FOLDER = 'output'
JSONPLACEHOLDER_BASE_URL = "https://jsonplaceholder.typicode.com"
EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"


class HTTPStatusCodes(Enum):
    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    TOO_MANY_REUQESTS = 429
    INTERNAL_SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503


COMMENT_STRUCTURE = {
    "id": int,
    "postId": int,
    "name": str,
    "email": str,
    "body": str
}
